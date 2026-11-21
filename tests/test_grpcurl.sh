#!/bin/bash
# Script de testes com grpcurl para Calculadora Distribuída
# Autores: Gabriel Cortez e Italo Monte

echo "=== Testes da Calculadora Distribuída com grpcurl ==="
echo "Autores: Gabriel Cortez e Italo Monte"
echo

# Verificar se grpcurl está instalado
if ! command -v grpcurl &> /dev/null; then
    if [ -f ~/go/bin/grpcurl ]; then
        GRPCURL=~/go/bin/grpcurl
    else
        echo "grpcurl não está instalado. Instalando..."
        go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
        GRPCURL=~/go/bin/grpcurl
    fi
else
    GRPCURL=grpcurl
fi

# Endereço do servidor
SERVER="localhost:50051"

echo "1. Testando operações básicas:"
echo

echo "   Adição: 10 + 5"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 5}' $SERVER calculator.CalculatorService/Add
echo

echo "   Subtração: 10 - 5"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 5}' $SERVER calculator.CalculatorService/Sub
echo

echo "   Multiplicação: 10 * 5"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 5}' $SERVER calculator.CalculatorService/Mul
echo

echo "   Divisão: 10 / 5"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 5}' $SERVER calculator.CalculatorService/Div
echo

echo "2. Testando casos especiais:"
echo

echo "   Divisão por zero: 10 / 0"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 0}' $SERVER calculator.CalculatorService/Div
echo

echo "   Números decimais: 3.14 + 2.86"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 3.14, "b": 2.86}' $SERVER calculator.CalculatorService/Add
echo

echo "   Números negativos: 5 - 10"
$GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 5, "b": 10}' $SERVER calculator.CalculatorService/Sub
echo

echo "3. Testando operações complexas:"
echo

echo "   Expressão: (10 + 5) * 2"
# Primeiro: 10 + 5 = 15
RESULT1=$($GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 5}' $SERVER calculator.CalculatorService/Add | grep -o '"result":[^,]*' | cut -d':' -f2)
echo "   Passo 1: 10 + 5 = $RESULT1"

# Segundo: 15 * 2 = 30
RESULT2=$($GRPCURL -plaintext -import-path proto -proto proto/calculator.proto -d "{\"a\": $RESULT1, \"b\": 2}" $SERVER calculator.CalculatorService/Mul | grep -o '"result":[^,]*' | cut -d':' -f2)
echo "   Passo 2: $RESULT1 * 2 = $RESULT2"

echo
echo "=== Testes concluídos ==="
