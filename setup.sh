#!/bin/bash
# Script de inicialização da Calculadora Distribuída
# Autores: Gabriel Cortez e Italo Monte

echo "=== Calculadora Distribuída gRPC ==="
echo "Autores: Gabriel Cortez e Italo Monte"
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não está instalado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Instalar dependências
echo "Instalando dependências..."
pip3 install grpcio grpcio-tools protobuf

# Gerar código Python a partir do .proto
echo "Gerando código Python..."
python3 -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated proto/calculator.proto

# Tornar scripts executáveis
chmod +x tests/test_grpcurl.sh
chmod +x server/server.py
chmod +x client/client.py

echo
echo "=== Instalação concluída ==="
echo
echo "Para executar:"
echo "1. Servidor: python3 server/server.py"
echo "2. Cliente: python3 client/client.py"
echo "3. Testes: python3 tests/test_runner.py"
echo "4. grpcurl: ./tests/test_grpcurl.sh"
echo
echo "Para modo interativo do cliente:"
echo "python3 client/client.py --interactive"
