run0km-api.kavosoft.com {
    tls kverdecia@gmail.com
    proxy / unix:/home/ubuntu/run0km-fastapi/uvicorn.sock {
        fail_timeout 0
        transparent
    }
    header / {
        -Server
        Referrer-Policy "same-origin"
        X-XSS-Protection "1; mode=block"
        X-Content-Type-Options "nosniff"
    }
}
