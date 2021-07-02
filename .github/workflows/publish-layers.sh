#!/usr/bin/env bash

set -Eeuo pipefail

echo "using this bucket prefix - ${BUCKET_PREFIX}"

# BUILD_DIR references the required directory for packaging a Lambda Layer (https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
BUILD_DIR=python
# Temp directory for packaging pyTenable 
DIST_DIR=dist
PY36_DIST=$DIST_DIR/python36.zip
PY37_DIST=$DIST_DIR/python37.zip
PY38_DIST=$DIST_DIR/python38.zip

REGIONS=(
  ap-northeast-1
  ap-northeast-2
  ap-south-1
  ap-southeast-1
  ap-southeast-2
  ca-central-1
  eu-central-1
  eu-north-1
  eu-west-1
  eu-west-2
  eu-west-3
  sa-east-1
  us-east-1
  us-east-2
  us-west-1
  us-west-2
)

# Checks that an S3 bucket exists in each region with the supplied bucket prefix and region suffix. Script will fail if buckets don't exist.
for region in "${REGIONS[@]}"; do
    bucket_name="${BUCKET_PREFIX}-${region}"
    aws --region $region s3 ls "s3://${bucket_name}"
done

function build-python36 {
    echo "Building pyTenable layer for python3.6"
    # Removes existing build and dist directories in case they are present.
    if [ -d "$BUILD_DIR" ]; then rm -rf $BUILD_DIR; fi
    if [ -d "$PY36_DIST" ]; then rm -rf $PY36_DIST; fi
    if [ -d "$DIST_DIR" ]; then rm -rf $DIST_DIR; fi
    mkdir -p $DIST_DIR

    # Uses docker container supplied by AWS to build for a specific version of Python in the same environment as the AWS Lambda service
    docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.6" /bin/sh -c "pip install pyTenable -t python/lib/python3.6/site-packages/; exit"
    # Creates archive and removes build directory in preparation of uploading to S3 and publishing the layer.
    zip -rq $PY36_DIST $BUILD_DIR
    sudo rm -rf $BUILD_DIR
    echo "Build complete: ${PY36_DIST}"
}

function publish-python36 {
    if [ ! -f $PY36_DIST ]; then
        echo "Package not found: ${PY36_DIST}"
        exit 1
    fi

    # Uses an MD5 hash to produce a unique key to avoid naming collisions on existing objects in the bucket
    py36_hash=$(md5sum $PY36_DIST | awk '{ print $1 }')
    py36_s3key="pyTenable-python3.6/${py36_hash}.zip"

    for region in "${REGIONS[@]}"; do
        bucket_name="${BUCKET_PREFIX}-${region}"

        # Copies Lambda Layer archive to the appropriate region bucket and uses an MD5 hash to produce a unique key to avoid naming collisions on existing objects in the bucket.
        echo "Uploading ${PY36_DIST} to s3://${bucket_name}/${py36_s3key}"
        aws --region $region s3 cp $PY36_DIST "s3://${bucket_name}/${py36_s3key}"

        echo "Publishing python3.6 layer to ${region}"
        py36_version=$(aws lambda publish-layer-version \
            --layer-name pyTenablePython36 \
            --content "S3Bucket=${bucket_name},S3Key=${py36_s3key}" \
            --description "pyTenable Layer for Python 3.6" \
            --license-info "Apache-2.0" \
            --compatible-runtimes python3.6 \
            --region $region \
            --output text \
            --query Version)
        echo "published python3.6 layer version ${py36_version} to ${region}"

        # Sets Lambda Layer to public so that anyone can use within their own Lambda functions
        echo "Setting public permissions for python3.6 layer version ${py36_version} in ${region}"
        aws lambda add-layer-version-permission \
          --layer-name pyTenablePython36 \
          --version-number $py36_version \
          --statement-id public \
          --action lambda:GetLayerVersion \
          --principal "*" \
          --region $region
        echo "Public permissions set for python3.6 layer version ${py36_version} in region ${region}"
    done
}

function build-python37 {
    echo "Building pyTenable layer for python3.7"
    # Removes existing build and dist directories in case they are present.
    if [ -d "$BUILD_DIR" ]; then rm -rf $BUILD_DIR; fi
    if [ -d "$PY36_DIST" ]; then rm -rf $PY36_DIST; fi
    if [ -d "$DIST_DIR" ]; then rm -rf $DIST_DIR; fi
    mkdir -p $DIST_DIR
    # Uses docker container supplied by AWS to build for a specific version of Python in the same environment as the AWS Lambda service
    docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.7" /bin/sh -c "pip install pyTenable -t python/lib/python3.7/site-packages/; exit"
    # Creates archive and removes build directory in preparation of uploading to S3 and publishing the layer.
    zip -rq $PY37_DIST $BUILD_DIR 
    sudo rm -rf $BUILD_DIR
    echo "Build complete: ${PY37_DIST}"
}

function publish-python37 {
    if [ ! -f $PY37_DIST ]; then
        echo "Package not found: ${PY37_DIST}"
        exit 1
    fi

    # Uses an MD5 hash to produce a unique key to avoid naming collisions on existing objects in the bucket
    py37_hash=$(md5sum $PY37_DIST | awk '{ print $1 }')
    py37_s3key="pyTenable-python3.7/${py37_hash}.zip"

    for region in "${REGIONS[@]}"; do
        bucket_name="${BUCKET_PREFIX}-${region}"

        # Copies Lambda Layer archive to the appropriate region bucket and uses an MD5 hash to produce a unique key to avoid naming collisions on existing objects in the bucket.
        echo "Uploading ${PY37_DIST} to s3://${bucket_name}/${py37_s3key}"
        aws --region $region s3 cp $PY37_DIST "s3://${bucket_name}/${py37_s3key}"

        echo "Publishing python3.7 layer to ${region}"
        py37_version=$(aws lambda publish-layer-version \
            --layer-name pyTenablePython37 \
            --content "S3Bucket=${bucket_name},S3Key=${py37_s3key}" \
            --description "pyTenable Layer for Python 3.7" \
            --license-info "Apache-2.0" \
            --compatible-runtimes python3.7 \
            --region $region \
            --output text \
            --query Version)
        echo "published python3.7 layer version ${py37_version} to ${region}"

        # Sets Lambda Layer to public so that anyone can use within their own Lambda functions
        echo "Setting public permissions for python3.7 layer version ${py37_version} in ${region}"
        aws lambda add-layer-version-permission \
          --layer-name pyTenablePython37 \
          --version-number $py37_version \
          --statement-id public \
          --action lambda:GetLayerVersion \
          --principal "*" \
          --region $region
        echo "Public permissions set for python3.7 layer version ${py37_version} in region ${region}"
    done
}

function build-python38 {
    echo "Building pyTenable layer for python3.8"
    # Removes existing build and dist directories in case they are present.
    if [ -d "$BUILD_DIR" ]; then rm -rf $BUILD_DIR; fi
    if [ -d "$PY36_DIST" ]; then rm -rf $PY36_DIST; fi
    if [ -d "$DIST_DIR" ]; then rm -rf $DIST_DIR; fi
    mkdir -p $DIST_DIR
    # Uses docker container supplied by AWS to build for a specific version of Python in the same environment as the AWS Lambda service
    docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.8" /bin/sh -c "pip install pyTenable -t python/lib/python3.8/site-packages/; exit"
    # Creates archive and removes build directory in preparation of uploading to S3 and publishing the layer.
    zip -rq $PY38_DIST $BUILD_DIR 
    sudo rm -rf $BUILD_DIR 
    echo "Build complete: ${PY38_DIST}"
}

function publish-python38 {
    if [ ! -f $PY38_DIST ]; then
        echo "Package not found: ${PY38_DIST}"
        exit 1
    fi

    # Uses an MD5 hash to produce a unique key to avoid naming collisions on existing objects in the bucket
    py38_hash=$(md5sum $PY38_DIST | awk '{ print $1 }')
    py38_s3key="pyTenable-python3.8/${py38_hash}.zip"

    for region in "${REGIONS[@]}"; do
        bucket_name="${BUCKET_PREFIX}-${region}"

        # Copies Lambda Layer archive to the appropriate region bucket and uses an MD5 hash to produce a unique key to avoid naming collisions on existing objects in the bucket. 
        echo "Uploading ${PY38_DIST} to s3://${bucket_name}/${py38_s3key}"
        aws --region $region s3 cp $PY38_DIST "s3://${bucket_name}/${py38_s3key}"


        echo "Publishing python3.8 layer to ${region}"
        py38_version=$(aws lambda publish-layer-version \
            --layer-name pyTenablePython38 \
            --content "S3Bucket=${bucket_name},S3Key=${py38_s3key}" \
            --description "pyTenable Layer for Python 3.8" \
            --license-info "Apache-2.0" \
            --compatible-runtimes python3.8 \
            --region $region \
            --output text \
            --query Version)
        echo "published python3.8 layer version ${py38_version} to ${region}"

        # Sets Lambda Layer to public so that anyone can use within their own Lambda functions
        echo "Setting public permissions for python3.8 layer version ${py38_version} in ${region}"
        aws lambda add-layer-version-permission \
          --layer-name pyTenablePython38 \
          --version-number $py38_version \
          --statement-id public \
          --action lambda:GetLayerVersion \
          --principal "*" \
          --region $region
        echo "Public permissions set for python3.8 layer version ${py38_version} in region ${region}"
    done
}

case "$1" in
    "python3.6")
        build-python36
        publish-python36
        ;;
    "python3.7")
        build-python37
        publish-python37
        ;;
    "python3.8")
        build-python38
        publish-python38
        ;;
    *)
        usage
        ;;
esac