# MongoDB configuration
MONGO_USER = "44c8dfaa"
MONGO_PASSWORD = "c08f8fc19dfd"
MONGO_DATABASE = "stockscreener"
MONGO_HOST = "ssdb.sblzd.cn"
MONGO_PORT = "65278"

# For backward compatibility (can be removed later)
FUTConfig = {
    "mt5_path": FUT_MT5_PATH,
    "warn_user": FUT_WARN_USER,
    "email_pwd": FUT_EMAIL_PWD,
    "email_user": FUT_EMAIL_USER,
    "email_reception": FUT_EMAIL_RECEPTION,
    "extra": {
        "tq_user": FUT_TQ_USER,
        "tq_pwd": FUT_TQ_PWD,
    },
}

FXConfig = {
    "mt5_path": FX_MT5_PATH,
    "warn_user": FX_WARN_USER,
    "email_pwd": FX_EMAIL_PWD,
    "email_user": FX_EMAIL_USER,
    "email_reception": FX_EMAIL_RECEPTION,
    "extra": {},
}

STKConfig = {
    "mt5_path": STK_MT5_PATH,
    "warn_user": STK_WARN_USER,
    "email_pwd": STK_EMAIL_PWD,
    "email_user": STK_EMAIL_USER,
    "email_reception": STK_EMAIL_RECEPTION,
    "extra": {},
} 