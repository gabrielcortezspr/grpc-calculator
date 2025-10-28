#!/usr/bin/env python3
"""
Servidor gRPC para Calculadora Distribuída
Autores: Gabriel Cortez e Italo Monte

Implementa operações básicas de calculadora com interceptors de log e validação.
"""

import grpc
import logging
import sys
import os
from concurrent import futures
from typing import Any, Callable, Iterator

# Adicionar o diretório generated ao path para importar os módulos gerados
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generated'))

import calculator_pb2
import calculator_pb2_grpc

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoggingInterceptor(grpc.ServerInterceptor):
    """
    Interceptor para logging de requisições e respostas gRPC
    """
    
    def intercept_service(self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler:
        """Intercepta chamadas de serviço para adicionar logging"""
        
        def logging_wrapper(behavior: Callable, request_streaming: bool, response_streaming: bool) -> Callable:
            """Wrapper para adicionar logging às operações"""
            
            if request_streaming and response_streaming:
                def bidi_streaming_handler(request_iterator: Iterator[Any], context: grpc.ServicerContext) -> Iterator[Any]:
                    logger.info(f"Iniciando chamada bidirecional: {handler_call_details.method}")
                    try:
                        for response in behavior(request_iterator, context):
                            logger.info(f"Resposta enviada: {response}")
                            yield response
                        logger.info(f"Chamada bidirecional concluída: {handler_call_details.method}")
                    except Exception as e:
                        logger.error(f"Erro na chamada bidirecional {handler_call_details.method}: {e}")
                        raise
                return bidi_streaming_handler
                
            elif request_streaming:
                def request_streaming_handler(request_iterator: Iterator[Any], context: grpc.ServicerContext) -> Any:
                    logger.info(f"Iniciando chamada com streaming de requisição: {handler_call_details.method}")
                    try:
                        response = behavior(request_iterator, context)
                        logger.info(f"Resposta enviada: {response}")
                        logger.info(f"Chamada com streaming de requisição concluída: {handler_call_details.method}")
                        return response
                    except Exception as e:
                        logger.error(f"Erro na chamada com streaming de requisição {handler_call_details.method}: {e}")
                        raise
                return request_streaming_handler
                
            elif response_streaming:
                def response_streaming_handler(request: Any, context: grpc.ServicerContext) -> Iterator[Any]:
                    logger.info(f"Iniciando chamada com streaming de resposta: {handler_call_details.method}")
                    logger.info(f"Requisição recebida: {request}")
                    try:
                        for response in behavior(request, context):
                            logger.info(f"Resposta enviada: {response}")
                            yield response
                        logger.info(f"Chamada com streaming de resposta concluída: {handler_call_details.method}")
                    except Exception as e:
                        logger.error(f"Erro na chamada com streaming de resposta {handler_call_details.method}: {e}")
                        raise
                return response_streaming_handler
                
            else:
                def unary_handler(request: Any, context: grpc.ServicerContext) -> Any:
                    logger.info(f"Iniciando chamada unária: {handler_call_details.method}")
                    logger.info(f"Requisição recebida: {request}")
                    try:
                        response = behavior(request, context)
                        logger.info(f"Resposta enviada: {response}")
                        logger.info(f"Chamada unária concluída: {handler_call_details.method}")
                        return response
                    except Exception as e:
                        logger.error(f"Erro na chamada unária {handler_call_details.method}: {e}")
                        raise
                return unary_handler
        
        # Obter o handler original
        handler = continuation(handler_call_details)
        if not handler:
            return None
        
        # Aplicar wrapper apenas para chamadas unárias
        if handler.unary_unary:
            return grpc.unary_unary_rpc_method_handler(
                logging_wrapper(handler.unary_unary, False, False)
            )
        elif handler.unary_stream:
            return grpc.unary_stream_rpc_method_handler(
                logging_wrapper(handler.unary_stream, False, True)
            )
        elif handler.stream_unary:
            return grpc.stream_unary_rpc_method_handler(
                logging_wrapper(handler.stream_unary, True, False)
            )
        elif handler.stream_stream:
            return grpc.stream_stream_rpc_method_handler(
                logging_wrapper(handler.stream_stream, True, True)
            )
        
        return handler


class ValidationInterceptor(grpc.ServerInterceptor):
    """
    Interceptor para validação de entrada
    """
    
    def intercept_service(self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler:
        """Intercepta chamadas de serviço para validação"""
        
        def validation_wrapper(behavior: Callable, request_streaming: bool, response_streaming: bool) -> Callable:
            """Wrapper para validação de entrada"""
            
            def unary_handler(request: Any, context: grpc.ServicerContext) -> Any:
                # Validar entrada para operações de calculadora
                if hasattr(request, 'a') and hasattr(request, 'b'):
                    if not isinstance(request.a, (int, float)) or not isinstance(request.b, (int, float)):
                        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                        context.set_details('Os operandos devem ser números válidos')
                        logger.warning(f"Validação falhou: operandos inválidos - a={request.a}, b={request.b}")
                        return None
                    
                    # Validação específica para divisão por zero
                    if handler_call_details.method.endswith('/Div') and request.b == 0:
                        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                        context.set_details('Divisão por zero não é permitida')
                        logger.warning(f"Tentativa de divisão por zero: a={request.a}, b={request.b}")
                        return None
                
                return behavior(request, context)
            
            return unary_handler
        
        # Obter o handler original
        handler = continuation(handler_call_details)
        if not handler:
            return None
        
        # Aplicar wrapper apenas para chamadas unárias
        if handler.unary_unary:
            return grpc.unary_unary_rpc_method_handler(
                validation_wrapper(handler.unary_unary, False, False)
            )
        
        return handler


class CalculatorServicer(calculator_pb2_grpc.CalculatorServiceServicer):
    """
    Implementação do serviço de calculadora
    """
    
    def Add(self, request: calculator_pb2.OperationRequest, context: grpc.ServicerContext) -> calculator_pb2.OperationResponse:
        """Implementa operação de adição"""
        try:
            result = request.a + request.b
            logger.info(f"Adição realizada: {request.a} + {request.b} = {result}")
            return calculator_pb2.OperationResponse(
                result=result,
                operation="Add",
                success=True,
                error_message=""
            )
        except Exception as e:
            logger.error(f"Erro na adição: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro interno: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0.0,
                operation="Add",
                success=False,
                error_message=str(e)
            )
    
    def Sub(self, request: calculator_pb2.OperationRequest, context: grpc.ServicerContext) -> calculator_pb2.OperationResponse:
        """Implementa operação de subtração"""
        try:
            result = request.a - request.b
            logger.info(f"Subtração realizada: {request.a} - {request.b} = {result}")
            return calculator_pb2.OperationResponse(
                result=result,
                operation="Sub",
                success=True,
                error_message=""
            )
        except Exception as e:
            logger.error(f"Erro na subtração: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro interno: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0.0,
                operation="Sub",
                success=False,
                error_message=str(e)
            )
    
    def Mul(self, request: calculator_pb2.OperationRequest, context: grpc.ServicerContext) -> calculator_pb2.OperationResponse:
        """Implementa operação de multiplicação"""
        try:
            result = request.a * request.b
            logger.info(f"Multiplicação realizada: {request.a} * {request.b} = {result}")
            return calculator_pb2.OperationResponse(
                result=result,
                operation="Mul",
                success=True,
                error_message=""
            )
        except Exception as e:
            logger.error(f"Erro na multiplicação: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro interno: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0.0,
                operation="Mul",
                success=False,
                error_message=str(e)
            )
    
    def Div(self, request: calculator_pb2.OperationRequest, context: grpc.ServicerContext) -> calculator_pb2.OperationResponse:
        """Implementa operação de divisão"""
        try:
            # Validação de divisão por zero
            if request.b == 0:
                logger.warning(f"Tentativa de divisão por zero: a={request.a}, b={request.b}")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Divisão por zero não é permitida')
                return calculator_pb2.OperationResponse(
                    result=0.0,
                    operation="Div",
                    success=False,
                    error_message="Divisão por zero não é permitida"
                )
            
            result = request.a / request.b
            logger.info(f"Divisão realizada: {request.a} / {request.b} = {result}")
            return calculator_pb2.OperationResponse(
                result=result,
                operation="Div",
                success=True,
                error_message=""
            )
        except Exception as e:
            logger.error(f"Erro na divisão: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro interno: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0.0,
                operation="Div",
                success=False,
                error_message=str(e)
            )


def serve():
    """Inicia o servidor gRPC"""
    # Configurar servidor sem interceptors por enquanto
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Adicionar serviço
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorServicer(), server)
    
    # Configurar porta
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    # Iniciar servidor
    server.start()
    logger.info(f"Servidor gRPC iniciado em {listen_addr}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Parando servidor...")
        server.stop(0)


if __name__ == '__main__':
    serve()
