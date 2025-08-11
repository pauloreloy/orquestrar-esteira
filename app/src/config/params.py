AWS_REGION              = "us-east-1"
AWS_ACCESS_KEY_ID       = None
AWS_ACCESS_SECRET_KEY   = None
AWS_ENDPOINT            = "localhost:4566"

LAMBDA_LOG_GROUP        = "JP3-RETENCAO"
LAMBDA_NAME             = "lbd-orquestrar-esteira-retencao"

TOGGLE_SCHEMAS          = "toggle-schemas-maquinas-de-estado"
TOGGLE_DEFAULT          = {
    "ValidaRetido":         "validacao-2",
    "RegistroEvidencia":    "registrar-evidencia"
}