#!/usr/bin/env python3
"""
Cliente gRPC para Calculadora Distribuída
Autores: Gabriel Cortez e Italo Monte

Cliente para testar as operações da calculadora distribuída.
"""

import grpc
import sys
import os
import logging

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


class CalculatorClient:
    """
    Cliente para o serviço de calculadora gRPC
    """
    
    def __init__(self, server_address: str = 'localhost:50051'):
        """
        Inicializa o cliente
        
        Args:
            server_address: Endereço do servidor gRPC
        """
        self.server_address = server_address
        self.channel = None
        self.stub = None
    
    def connect(self):
        """Conecta ao servidor gRPC"""
        try:
            self.channel = grpc.insecure_channel(self.server_address)
            self.stub = calculator_pb2_grpc.CalculatorServiceStub(self.channel)
            logger.info(f"Conectado ao servidor em {self.server_address}")
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            raise
    
    def disconnect(self):
        """Desconecta do servidor"""
        if self.channel:
            self.channel.close()
            logger.info("Desconectado do servidor")
    
    def add(self, a: float, b: float) -> calculator_pb2.OperationResponse:
        """
        Realiza operação de adição
        
        Args:
            a: Primeiro operando
            b: Segundo operando
            
        Returns:
            Resposta da operação
        """
        try:
            request = calculator_pb2.OperationRequest(a=a, b=b)
            response = self.stub.Add(request)
            logger.info(f"Adição: {a} + {b} = {response.result}")
            return response
        except grpc.RpcError as e:
            logger.error(f"Erro gRPC na adição: {e.code()} - {e.details()}")
            raise
    
    def sub(self, a: float, b: float) -> calculator_pb2.OperationResponse:
        """
        Realiza operação de subtração
        
        Args:
            a: Primeiro operando
            b: Segundo operando
            
        Returns:
            Resposta da operação
        """
        try:
            request = calculator_pb2.OperationRequest(a=a, b=b)
            response = self.stub.Sub(request)
            logger.info(f"Subtração: {a} - {b} = {response.result}")
            return response
        except grpc.RpcError as e:
            logger.error(f"Erro gRPC na subtração: {e.code()} - {e.details()}")
            raise
    
    def mul(self, a: float, b: float) -> calculator_pb2.OperationResponse:
        """
        Realiza operação de multiplicação
        
        Args:
            a: Primeiro operando
            b: Segundo operando
            
        Returns:
            Resposta da operação
        """
        try:
            request = calculator_pb2.OperationRequest(a=a, b=b)
            response = self.stub.Mul(request)
            logger.info(f"Multiplicação: {a} * {b} = {response.result}")
            return response
        except grpc.RpcError as e:
            logger.error(f"Erro gRPC na multiplicação: {e.code()} - {e.details()}")
            raise
    
    def div(self, a: float, b: float) -> calculator_pb2.OperationResponse:
        """
        Realiza operação de divisão
        
        Args:
            a: Primeiro operando
            b: Segundo operando
            
        Returns:
            Resposta da operação
        """
        try:
            request = calculator_pb2.OperationRequest(a=a, b=b)
            response = self.stub.Div(request)
            logger.info(f"Divisão: {a} / {b} = {response.result}")
            return response
        except grpc.RpcError as e:
            logger.error(f"Erro gRPC na divisão: {e.code()} - {e.details()}")
            raise


def run_tests():
    """
    Executa testes básicos do cliente
    """
    client = CalculatorClient()
    
    try:
        # Conectar ao servidor
        client.connect()
        
        print("=== Testes da Calculadora Distribuída ===")
        print("Autores: Gabriel Cortez e Italo Monte")
        print()
        
        # Teste 1: Operações básicas
        print("1. Testando operações básicas:")
        
        # Adição
        response = client.add(10, 5)
        print(f"   Adição: 10 + 5 = {response.result} (Sucesso: {response.success})")
        
        # Subtração
        response = client.sub(10, 5)
        print(f"   Subtração: 10 - 5 = {response.result} (Sucesso: {response.success})")
        
        # Multiplicação
        response = client.mul(10, 5)
        print(f"   Multiplicação: 10 * 5 = {response.result} (Sucesso: {response.success})")
        
        # Divisão
        response = client.div(10, 5)
        print(f"   Divisão: 10 / 5 = {response.result} (Sucesso: {response.success})")
        
        print()
        
        # Teste 2: Casos especiais
        print("2. Testando casos especiais:")
        
        # Divisão por zero
        try:
            response = client.div(10, 0)
            print(f"   Divisão por zero: 10 / 0 = {response.result} (Sucesso: {response.success})")
            if not response.success:
                print(f"   Erro: {response.error_message}")
        except grpc.RpcError as e:
            print(f"   Divisão por zero: Erro gRPC - {e.code()}: {e.details()}")
        
        # Números decimais
        response = client.add(3.14, 2.86)
        print(f"   Decimais: 3.14 + 2.86 = {response.result} (Sucesso: {response.success})")
        
        # Números negativos
        response = client.sub(5, 10)
        print(f"   Negativos: 5 - 10 = {response.result} (Sucesso: {response.success})")
        
        print()
        
        # Teste 3: Operações complexas
        print("3. Testando operações complexas:")
        
        # Expressão: (10 + 5) * 2 - 3
        step1 = client.add(10, 5)  # 15
        step2 = client.mul(step1.result, 2)  # 30
        step3 = client.sub(step2.result, 3)  # 27
        print(f"   Expressão (10 + 5) * 2 - 3 = {step3.result}")
        
        print()
        print("=== Todos os testes concluídos ===")
        
    except Exception as e:
        logger.error(f"Erro durante os testes: {e}")
        print(f"Erro: {e}")
    
    finally:
        # Desconectar
        client.disconnect()


def interactive_mode():
    """
    Modo interativo para o usuário testar operações
    """
    client = CalculatorClient()
    
    try:
        client.connect()
        print("=== Calculadora Distribuída - Modo Interativo ===")
        print("Autores: Gabriel Cortez e Italo Monte")
        print("Digite 'sair' para encerrar")
        print("Formato: operação a b (ex: add 10 5)")
        print("Operações: add, sub, mul, div")
        print()
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    break
                
                parts = user_input.split()
                if len(parts) != 3:
                    print("Formato inválido. Use: operação a b")
                    continue
                
                operation, a_str, b_str = parts
                
                try:
                    a = float(a_str)
                    b = float(b_str)
                except ValueError:
                    print("Os operandos devem ser números válidos")
                    continue
                
                if operation.lower() == 'add':
                    response = client.add(a, b)
                elif operation.lower() == 'sub':
                    response = client.sub(a, b)
                elif operation.lower() == 'mul':
                    response = client.mul(a, b)
                elif operation.lower() == 'div':
                    response = client.div(a, b)
                else:
                    print("Operação inválida. Use: add, sub, mul, div")
                    continue
                
                if response.success:
                    print(f"Resultado: {response.result}")
                else:
                    print(f"Erro: {response.error_message}")
                    
            except grpc.RpcError as e:
                print(f"Erro gRPC: {e.code()} - {e.details()}")
            except Exception as e:
                print(f"Erro: {e}")
    
    except Exception as e:
        logger.error(f"Erro no modo interativo: {e}")
        print(f"Erro ao conectar: {e}")
    
    finally:
        client.disconnect()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Cliente gRPC para Calculadora Distribuída')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Executa em modo interativo')
    parser.add_argument('--server', '-s', default='localhost:50051',
                       help='Endereço do servidor (padrão: localhost:50051)')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    else:
        run_tests()
