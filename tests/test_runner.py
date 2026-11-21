#!/usr/bin/env python3
"""
Script de testes automatizados para Calculadora Distribuída
Autores: Gabriel Cortez e Italo Monte

Executa testes automatizados do servidor e cliente gRPC.
"""

import subprocess
import time
import sys
import os
import signal
import threading
import requests
import json

# Adicionar o diretório generated ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generated'))

import calculator_pb2
import calculator_pb2_grpc
import grpc

class TestRunner:
    """Executa testes automatizados"""
    
    def __init__(self):
        self.server_process = None
        self.test_results = []
    
    def start_server(self):
        """Inicia o servidor gRPC em processo separado"""
        try:
            server_script = os.path.join(os.path.dirname(__file__), '..', 'server', 'server.py')
            self.server_process = subprocess.Popen(
                [sys.executable, server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Aguardar servidor inicializar
            time.sleep(3)
            
            if self.server_process.poll() is None:
                print("✓ Servidor iniciado com sucesso")
                return True
            else:
                print("✗ Falha ao iniciar servidor")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao iniciar servidor: {e}")
            return False
    
    def stop_server(self):
        """Para o servidor gRPC"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("✓ Servidor parado")
    
    def test_connection(self):
        """Testa conexão com o servidor"""
        try:
            channel = grpc.insecure_channel('localhost:50051')
            stub = calculator_pb2_grpc.CalculatorServiceStub(channel)
            
            # Teste simples
            request = calculator_pb2.OperationRequest(a=1, b=1)
            response = stub.Add(request)
            
            if response.success and response.result == 2:
                print("✓ Conexão com servidor funcionando")
                return True
            else:
                print("✗ Resposta inesperada do servidor")
                return False
                
        except Exception as e:
            print(f"✗ Erro de conexão: {e}")
            return False
    
    def test_basic_operations(self):
        """Testa operações básicas"""
        try:
            channel = grpc.insecure_channel('localhost:50051')
            stub = calculator_pb2_grpc.CalculatorServiceStub(channel)
            
            tests = [
                ("Add", 10, 5, 15),
                ("Sub", 10, 5, 5),
                ("Mul", 10, 5, 50),
                ("Div", 10, 5, 2),
            ]
            
            all_passed = True
            
            for operation, a, b, expected in tests:
                request = calculator_pb2.OperationRequest(a=a, b=b)
                
                if operation == "Add":
                    response = stub.Add(request)
                elif operation == "Sub":
                    response = stub.Sub(request)
                elif operation == "Mul":
                    response = stub.Mul(request)
                elif operation == "Div":
                    response = stub.Div(request)
                
                if response.success and abs(response.result - expected) < 0.001:
                    print(f"✓ {operation}({a}, {b}) = {response.result}")
                else:
                    print(f"✗ {operation}({a}, {b}) = {response.result} (esperado: {expected})")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            print(f"✗ Erro nos testes básicos: {e}")
            return False
    
    def test_error_cases(self):
        """Testa casos de erro"""
        try:
            channel = grpc.insecure_channel('localhost:50051')
            stub = calculator_pb2_grpc.CalculatorServiceStub(channel)
            
            # Teste divisão por zero
            request = calculator_pb2.OperationRequest(a=10, b=0)
            
            try:
                response = stub.Div(request)
                if not response.success and "zero" in response.error_message.lower():
                    print("✓ Divisão por zero detectada corretamente")
                    return True
                else:
                    print("✗ Divisão por zero não foi detectada")
                    return False
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    print("✓ Divisão por zero rejeitada pelo interceptor")
                    return True
                else:
                    print(f"✗ Erro inesperado na divisão por zero: {e}")
                    return False
                    
        except Exception as e:
            print(f"✗ Erro nos testes de erro: {e}")
            return False
    
    def test_performance(self):
        """Testa performance com múltiplas operações"""
        try:
            channel = grpc.insecure_channel('localhost:50051')
            stub = calculator_pb2_grpc.CalculatorServiceStub(channel)
            
            start_time = time.time()
            operations_count = 100
            
            for i in range(operations_count):
                request = calculator_pb2.OperationRequest(a=i, b=1)
                response = stub.Add(request)
                if not response.success:
                    print(f"✗ Falha na operação {i}")
                    return False
            
            end_time = time.time()
            duration = end_time - start_time
            ops_per_second = operations_count / duration
            
            print(f"✓ Performance: {ops_per_second:.2f} operações/segundo")
            return True
            
        except Exception as e:
            print(f"✗ Erro no teste de performance: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("=== Testes Automatizados da Calculadora Distribuída ===")
        print("Autores: Gabriel Cortez e Italo Monte")
        print()
        
        # Iniciar servidor
        if not self.start_server():
            return False
        
        try:
            # Aguardar servidor estar pronto
            time.sleep(2)
            
            # Executar testes
            tests = [
                ("Conexão", self.test_connection),
                ("Operações Básicas", self.test_basic_operations),
                ("Casos de Erro", self.test_error_cases),
                ("Performance", self.test_performance),
            ]
            
            passed = 0
            total = len(tests)
            
            for test_name, test_func in tests:
                print(f"\n--- {test_name} ---")
                if test_func():
                    passed += 1
            
            print(f"\n=== Resultados ===")
            print(f"Testes passaram: {passed}/{total}")
            print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
            
            return passed == total
            
        finally:
            self.stop_server()


def main():
    """Função principal"""
    runner = TestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTestes interrompidos pelo usuário")
        runner.stop_server()
        sys.exit(1)


if __name__ == '__main__':
    main()
