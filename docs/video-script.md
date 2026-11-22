# Instruções para Vídeo Explicativo - Calculadora Distribuída gRPC

## Autores da Dupla
- Gabriel Cortez
- Italo Monte

## Roteiro do Vídeo

### 1. Introdução (30 segundos)
**Texto para apresentação:**
"Olá! Somos Gabriel Cortez e Italo Monte, estudantes de Engenharia de Software. Hoje vamos apresentar nosso projeto de Calculadora Distribuída implementada usando gRPC em Python. Este projeto demonstra os conceitos fundamentais de comunicação distribuída através de chamadas de procedimento remoto (RPC) usando o protocolo gRPC."

### 2. Demonstração da Arquitetura (1 minuto)
**Texto para apresentação:**
"Vamos começar mostrando a arquitetura do nosso sistema. O gRPC utiliza Protocol Buffers para definir contratos de serviço. Aqui temos nosso arquivo calculator.proto que define quatro operações básicas: Add, Sub, Mul e Div. Cada operação recebe dois operandos (a e b) e retorna um resultado com informações sobre o sucesso da operação. 

O gRPC gera automaticamente código Python a partir deste arquivo .proto, criando classes para mensagens e stubs para comunicação cliente-servidor. Isso garante type safety e compatibilidade entre diferentes linguagens de programação.

Nossa implementação utiliza chamadas unárias, ou seja, uma requisição gera uma resposta, sem streaming. O servidor é stateless, não mantém estado entre requisições, o que facilita escalabilidade e distribuição."

### 3. Execução do Servidor (1 minuto)
**Texto para apresentação:**
"Agora vamos executar nosso servidor gRPC. O servidor é iniciado na porta 50051 e utiliza um thread pool com 10 workers para processar requisições concorrentemente. 

Observem os logs detalhados que implementamos - cada operação é registrada com timestamp, parâmetros de entrada e resultado. Isso é fundamental para debugging e monitoramento em sistemas distribuídos.

O servidor também implementa validação robusta, especialmente para prevenir divisão por zero, que é um caso crítico em sistemas de cálculo."

### 4. Testes com Cliente Python (2 minutos)
**Texto para apresentação:**
"Vamos testar nosso serviço usando nosso cliente Python customizado. Primeiro, testamos as operações básicas: adição, subtração, multiplicação e divisão com números inteiros.

Agora vamos demonstrar nossa validação de entrada - tentamos dividir por zero e o sistema retorna um erro gRPC apropriado com código INVALID_ARGUMENT, mantendo a integridade do sistema.

Testamos também números decimais e negativos, mostrando que nosso sistema é robusto para diferentes tipos de entrada numérica.

Por fim, demonstramos operações complexas combinando múltiplas chamadas gRPC para resolver expressões matemáticas mais elaboradas."

### 5. Testes com grpcurl (2 minutos)
**Texto para apresentação:**
"Uma das vantagens do gRPC é a facilidade de teste via linha de comando usando ferramentas como grpcurl. Vamos executar nosso script de testes automatizados.

O grpcurl permite testar serviços gRPC sem precisar escrever código cliente, apenas especificando o arquivo .proto e os dados JSON da requisição.

Observem como cada operação retorna uma resposta JSON estruturada com o resultado, tipo de operação e status de sucesso. Isso facilita integração com sistemas externos e debugging.

Novamente testamos a validação de divisão por zero, que retorna um erro HTTP apropriado com mensagem descritiva."

### 6. Testes Automatizados (1 minuto)
**Texto para apresentação:**
"Para garantir qualidade e confiabilidade, implementamos uma suíte completa de testes automatizados. Nosso test runner executa múltiplos cenários:

- Testes de conectividade e comunicação básica
- Validação de todas as operações matemáticas
- Casos de erro e tratamento de exceções
- Testes de performance com múltiplas operações simultâneas

Isso demonstra boas práticas de desenvolvimento de software distribuído, onde testes automatizados são essenciais para garantir a confiabilidade do sistema."

### 7. Conclusões (30 segundos)
**Texto para apresentação:**
"Em resumo, implementamos com sucesso uma calculadora distribuída usando gRPC que demonstra:

- Comunicação eficiente entre serviços usando Protocol Buffers
- Validação robusta de entrada e tratamento de erros
- Logging detalhado para monitoramento
- Testes abrangentes usando diferentes ferramentas
- Arquitetura stateless e escalável

Este projeto ilustra como o gRPC oferece vantagens sobre REST APIs tradicionais em termos de performance, type safety e facilidade de desenvolvimento. Obrigado pela atenção!"

## Pontos Importantes para Destacar

### Funcionalidades Implementadas ✅
- Serviço gRPC com operações básicas (Add, Sub, Mul, Div)
- Chamadas unárias (não streaming)
- Servidor stateless
- Validação de entrada (divisão por zero)
- Logging detalhado
- Testes com grpcurl
- Cliente Python para testes
- Testes automatizados

### Casos de Teste Demonstrados
1. **Operações Básicas**: 10 + 5, 10 - 5, 10 * 5, 10 / 5
2. **Validação de Erro**: Divisão por zero (10 / 0)
3. **Números Decimais**: 3.14 + 2.86
4. **Números Negativos**: 5 - 10
5. **Operações Complexas**: (10 + 5) * 2 - 3

### Comandos para Executar Durante o Vídeo

```bash
# 1. Instalar dependências
pip3 install grpcio grpcio-tools protobuf

# 2. Gerar código Python
python3 -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated proto/calculator.proto

# 3. Executar servidor
python3 server/server.py

# 4. Testar com cliente Python
python3 client/client.py

# 5. Testar com grpcurl
./tests/test_grpcurl.sh

# 6. Testes automatizados
python3 tests/test_runner.py
```

### Comandos grpcurl Individuais
```bash
# Adição
~/go/bin/grpcurl -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Add

# Divisão por zero (erro)
~/go/bin/grpcurl -plaintext -import-path proto -proto proto/calculator.proto -d '{"a": 10, "b": 0}' localhost:50051 calculator.CalculatorService/Div
```

## Fontes de Consulta
- Documentação oficial gRPC Python: https://grpc.io/docs/languages/python/
- Protocol Buffers: https://developers.google.com/protocol-buffers
- grpcurl: https://github.com/fullstorydev/grpcurl
- Interceptors gRPC: https://grpc.io/docs/languages/python/interceptors/

## Duração Total Estimada: 7-8 minutos
