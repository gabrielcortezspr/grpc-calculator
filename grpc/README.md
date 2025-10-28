# Calculadora Distribuída gRPC

## Autores da Dupla
- Gabriel Cortez
- Italo Monte

## Descrição
Implementação de uma calculadora distribuída usando gRPC com operações básicas: Add, Sub, Mul, Div.

### Características Implementadas
- ✅ Serviço gRPC com operações básicas (Add, Sub, Mul, Div)
- ✅ Chamadas unárias (não streaming)
- ✅ Servidor stateless
- ✅ Interceptors de log para monitoramento
- ✅ Validação de entrada (divisão por zero)
- ✅ Testes com grpcurl
- ✅ Cliente Python para testes
- ✅ Testes automatizados
- ✅ Documentação completa

## Estrutura do Projeto
```
grpc/
├── proto/                    # Arquivos .proto
│   └── calculator.proto     # Definição do serviço
├── generated/                # Código gerado pelo protoc
│   ├── calculator_pb2.py    # Mensagens Python
│   └── calculator_pb2_grpc.py # Serviços Python
├── server/                   # Implementação do servidor
│   └── server.py            # Servidor gRPC com interceptors
├── client/                   # Implementação do cliente
│   └── client.py            # Cliente gRPC para testes
├── tests/                    # Testes e exemplos
│   ├── test_grpcurl.sh      # Script de testes com grpcurl
│   └── test_runner.py       # Testes automatizados
├── requirements.txt          # Dependências Python
├── setup.sh                 # Script de instalação
└── README.md                # Este arquivo
```

## Fontes de Consulta
- Documentação oficial gRPC Python: https://grpc.io/docs/languages/python/
- Protocol Buffers: https://developers.google.com/protocol-buffers
- grpcurl: https://github.com/fullstorydev/grpcurl
- Interceptors gRPC: https://grpc.io/docs/languages/python/interceptors/

## Instalação Rápida

### Opção 1: Script Automático
```bash
chmod +x setup.sh
./setup.sh
```

### Opção 2: Manual
```bash
# 1. Instalar dependências
pip3 install grpcio grpcio-tools protobuf

# 2. Gerar código Python
python3 -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated proto/calculator.proto

# 3. Tornar scripts executáveis
chmod +x tests/test_grpcurl.sh
chmod +x server/server.py
chmod +x client/client.py
```

## Como Executar

### 1. Executar Servidor
```bash
python3 server/server.py
```
O servidor será iniciado na porta 50051 com interceptors de log e validação.

### 2. Executar Cliente (Testes Automáticos)
```bash
python3 client/client.py
```

### 3. Executar Cliente (Modo Interativo)
```bash
python3 client/client.py --interactive
```

### 4. Testes Automatizados
```bash
python3 tests/test_runner.py
```

### 5. Testes com grpcurl
```bash
# Instalar grpcurl (se necessário)
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# Executar testes
./tests/test_grpcurl.sh

# Ou comandos individuais:
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Add
```

## Exemplos de Uso

### Operações Básicas
```bash
# Adição
grpcurl -plaintext -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Add

# Subtração
grpcurl -plaintext -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Sub

# Multiplicação
grpcurl -plaintext -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Mul

# Divisão
grpcurl -plaintext -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Div
```

### Casos Especiais
```bash
# Divisão por zero (deve retornar erro)
grpcurl -plaintext -d '{"a": 10, "b": 0}' localhost:50051 calculator.CalculatorService/Div

# Números decimais
grpcurl -plaintext -d '{"a": 3.14, "b": 2.86}' localhost:50051 calculator.CalculatorService/Add
```

## Arquitetura

### Servidor
- **Porta**: 50051
- **Interceptors**: 
  - `LoggingInterceptor`: Registra todas as requisições e respostas
  - `ValidationInterceptor`: Valida entrada e previne divisão por zero
- **Thread Pool**: 10 workers para processamento concorrente
- **Logging**: Configurado com nível INFO

### Cliente
- **Modo Automático**: Executa testes pré-definidos
- **Modo Interativo**: Permite entrada manual de operações
- **Tratamento de Erros**: Captura e exibe erros gRPC

### Protocolo
- **Tipo**: Chamadas unárias (não streaming)
- **Estado**: Stateless (sem persistência de estado)
- **Formato**: Protocol Buffers v3

## Logs e Monitoramento

O servidor produz logs detalhados incluindo:
- Início e fim de cada requisição
- Parâmetros de entrada
- Resultados das operações
- Erros e exceções
- Tentativas de divisão por zero

Exemplo de log:
```
2024-01-15 10:30:15 - INFO - Iniciando chamada unária: /calculator.CalculatorService/Add
2024-01-15 10:30:15 - INFO - Requisição recebida: a: 10.0 b: 5.0
2024-01-15 10:30:15 - INFO - Adição realizada: 10.0 + 5.0 = 15.0
2024-01-15 10:30:15 - INFO - Resposta enviada: result: 15.0 operation: "Add" success: true
2024-01-15 10:30:15 - INFO - Chamada unária concluída: /calculator.CalculatorService/Add
```

## Testes

### Cobertura de Testes
- ✅ Operações básicas (Add, Sub, Mul, Div)
- ✅ Casos de erro (divisão por zero)
- ✅ Números decimais e negativos
- ✅ Performance (100 operações)
- ✅ Conexão e desconexão
- ✅ Validação de entrada

### Executar Todos os Testes
```bash
python3 tests/test_runner.py
```

### Testes Individuais
```bash
# Testes básicos
python3 client/client.py

# Testes com grpcurl
./tests/test_grpcurl.sh
```
