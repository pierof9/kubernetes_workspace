1. Build an Image
```bash
docker build --build-arg DB_USERNAME=<DB_USERNAME> --build-arg DB_PASSWORD=<DB_PASSWORD> -t coworking-checkin .
```
Sometimes if you don't find your changes propagating, you might need to add the flag `--no-cache`.

2. Run a Container
```bash
docker run -e DB_USERNAME=<DB_USERNAME> -e DB_PASSWORD=<DB_PASSWORD> -p 5151:5151 <CONTAINER_NAME>
```

## The "Analytics" application here is handled in two steps:
### Continuous Build process through AWS CodeBuild
...

### Application deployment with kubectl
...