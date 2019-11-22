## Docker build
```
docker build -t cuda9-ubuntu1604 .
```

## Docker run
```
docker run \
	--interactive \
	--tty \
	--rm \
	--runtime=nvidia \
  --volume /home/user/va-workspace/tracking_wo_bnw/docker/resources/output:/home/user/tracking_wo_bnw/output \
  --volume /home/user/va-workspace/tracking_wo_bnw/docker/resources/data:/home/user/tracking_wo_bnw/data \
	cuda9-ubuntu1604
```
