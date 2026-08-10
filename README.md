# Gerenciador de Contratos PNCP

Sistema desenvolvido em Python para consulta de contratos publicados no Portal Nacional de Contratações Públicas (PNCP), gerenciamento de contatos e envio automatizado de notificações via WhatsApp.

## Sobre o projeto

O sistema foi desenvolvido para automatizar o acompanhamento de contratos do PNCP.

A aplicação consulta periodicamente os contratos disponibilizados pela API do PNCP, identifica contratos ainda não notificados, associa cada contrato à sua unidade de destino e realiza o envio das notificações via WhatsApp.

Além das notificações individuais, o sistema também possui um relatório consolidado destinado ao comandante, contendo os contratos enviados durante a sessão.

## Funcionalidades

- Consulta de contratos através da API do PNCP
- Paginação dos resultados da API
- Identificação da unidade através do objeto do contrato
- Controle de contratos já notificados
- Persistência local utilizando SQLite
- Gerenciamento de contatos através de interface gráfica
- Cadastro e atualização do telefone do comandante
- Envio automático de mensagens via WhatsApp
- Relatório consolidado dos contratos enviados
- Suporte a redes com autenticação de proxy
- Solicitação dinâmica das credenciais de proxy
- Tratamento de indisponibilidade da API
- Interface gráfica desenvolvida com Tkinter
- Compatibilidade com execução através de arquivo `.exe`

## Tecnologias

- Python
- Requests
- Selenium
- Tkinter
- SQLite
- PNCP API
- PyInstaller

## Arquitetura

O projeto utiliza uma organização baseada em separação de responsabilidades.

### Clients

Responsáveis pela comunicação com serviços externos.

- `PNCPClient`: comunicação com a API do PNCP
- `WhatsAppClient`: automação do envio de mensagens

### Models

Representação dos dados utilizados pela aplicação.

- `Contract`: modelo de contrato

### Repositories

Responsáveis pela persistência e acesso aos dados.

- `ContractRepository`
- `SettingsRepository`

### Services

Contém as regras de negócio da aplicação.

- `NotificationService`

### UI

Interface gráfica da aplicação.

- Tela principal
- Gerenciamento de contatos

### Database

Responsável pela criação e conexão com o banco SQLite.

## Fluxo da aplicação

```text
             ┌─────────────────┐
             │    PNCP API     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   PNCPClient    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │     Contract    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Notification    │
             │    Service      │
             └───────┬─┬───────┘
                     │ │
             ┌───────┘ └────────┐
             ▼                  ▼
      ┌──────────────┐   ┌──────────────┐
      │    SQLite    │   │   WhatsApp   │
      │   Database   │   │   Selenium   │
      └──────────────┘   └──────────────┘