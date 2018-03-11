import arrow


class S3Object:
    def __init__(self, etag: str, sequencer: str, key: str, size: float):
        self._etag = etag
        self._sequencer = sequencer
        self._key = key
        self._size = size

    @classmethod
    def from_json(cls, obj):
        return cls(obj.get("eTag", None),
                   obj.get("sequencer", None),
                   obj["key"],
                   obj["size"])

    @property
    def etag(self):
        return self._etag

    @property
    def sequencer(self):
        return self._sequencer

    @property
    def key(self):
        return self._key

    @property
    def size(self):
        return self._size


class S3Bucket:
    def __init__(self, arn: str, name: str, owner_identity: str):
        self._arn = arn
        self._name = name
        self._owner_identity = owner_identity

    @classmethod
    def from_json(cls, bucket):
        return cls(bucket["arn"],
                   bucket["name"],
                   bucket["ownerIdentity"])

    @property
    def arn(self):
        return self._arn

    @property
    def name(self):
        return self._name

    @property
    def owner_identity(self):
        return self._owner_identity


class S3():
    def __init__(self, configuration_id: str, obj: S3Object, bucket: S3Bucket, s3_schemaversion: str):
        self._configuration_id = configuration_id
        self._object = obj
        self._bucket = bucket
        self._s3_schemaversion = s3_schemaversion

    @classmethod
    def from_json(cls, s3):
        return cls(s3["configurationId"],
                   S3Object.from_json(s3["object"]),
                   S3Bucket.from_json(s3["bucket"]),
                   s3["s3SchemaVersion"])

    @property
    def configuration_id(self):
        return self._configuration_id

    @property
    def object(self):
        return self._object

    @property
    def bucket(self):
        return self._bucket

    @property
    def s3_schemaversion(self):
        return self._s3_schemaversion


class S3Record:
    def __init__(self, event_version: str,
                 event_time: str,
                 request_params: dict,
                 s3: S3,
                 response_elements: dict,
                 aws_region: str,
                 event_name: str,
                 user_identity: dict,
                 event_source: str):
        self._event_version = event_version
        self._event_time = arrow.get(event_time)
        self._event_name = event_name
        self._event_source = event_source
        self._request_params = request_params
        self._s3 = s3
        self._response_elements = response_elements
        self._aws_region = aws_region
        self._user_identity = user_identity

    @classmethod
    def from_json(cls, record):
        return cls(record["eventVersion"],
                   record["eventTime"],
                   record["requestParameters"],
                   S3.from_json(record["s3"]),
                   record["responseElements"],
                   record["awsRegion"],
                   record["eventName"],
                   record["userIdentity"],
                   record["eventSource"])

    @property
    def event_version(self):
        return self._event_version

    @property
    def event_time(self):
        return self._event_time

    @property
    def s3(self):
        return self._s3

    @property
    def request_params(self):
        return self._request_params

    @property
    def response_elements(self):
        return self._response_elements

    @property
    def aws_region(self):
        return self._aws_region

    @property
    def event_name(self):
        return self._event_name

    @property
    def user_identity(self):
        return self._user_identity

    @property
    def event_source(self):
        return self._event_source


class S3Event:
    def __init__(self, records: [S3Record]):
        self._records = records

    @classmethod
    def from_event(cls, event):
        return cls([S3Record.from_json(record) for record in event["Records"]])

    @property
    def records(self) -> [S3Record]:
        return self._records

    @property
    def first_record(self) -> S3Record:
        return self._records[0]
