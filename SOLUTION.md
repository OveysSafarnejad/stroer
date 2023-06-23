# Synchronizing JSONPlaceholder Database with Ströer

## Background

In this exercise, the objective is to synchronize the data between the
JSONPlaceholder website and the Ströer application's database. Initially, all
the data from the JSONPlaceholder website is loaded into the Ströer database.
Subsequently, any changes made to the Ströer database are asynchronously
applied to the JSONPlaceholder database.

---

## Solution

To accomplish the aforementioned tasks, the following steps are taken in the
background:

1. First, commands are executed on the Ströer server to load the initial data
   into its database.

```commandline
python manage.py fetch_posts
python manage.py fetch_comments
```

Note the order of execution.

2. In the second step, the data in the Ströer database can be modified through
   the following REST endpoints:

```pseudocode
stroer_host:port/posts/                    (POST)
stroer_host:port/posts/:id/                (GET)
stroer_host:port/posts/:id/comments/       (GET)
stroer_host:port/posts/?title='post title' (GET)
stroer_host:port/posts/:id/                (DELETE)
stroer_host:port/posts/:id/                (PUT)

stroer_host:port/comments/                 (POST)
stroer_host:port/comments/:id/             (GET)
stroer_host:port/comments/?postId=1        (GET)
stroer_host:port/comments/:id/             (DELETE)
stroer_host:port/comments/:id/             (PUT)
```

3. Certain endpoints allow data manipulation, and Django model signals (
   implemented using the Observer design pattern) capture the changes made to
   the Ströer database. The captured changes are logged using a logger. The
   following receivers handle these signals:

```python
@receiver(
   signal=post_save,
   sender=Post,
   dispatch_uid='save_post_call_back'
)
@receiver(
   signal=post_save,
   sender=Comment,
   dispatch_uid='save_comment_call_back'
)
def save_model_callback(sender, instance, created, **kwargs):


# Code for handling the signal and logging the changes

@receiver(
   signal=post_delete,
   sender=Post,
   dispatch_uid='delete_post_call_back'
)
@receiver(
   signal=post_delete,
   sender=Comment,
   dispatch_uid='delete_comment_call_back'
)
def delete_model_callback(sender, instance, **kwargs):
# Code for handling the signal and logging the changes
```

By running updates, creations, or deletions on models, log records are
generated for the corresponding instances.

```
{"event": 0, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "created_time": "2023-06-20 13:23:30.360106+00:00", "modified_time": "2023-06-20 13:23:30.360147+00:00", "creator_id": null, "modifier_id": null, "api_post_id": null, "title": "post2", "body": "Hallo!", "user_id": 99999942}}
{"event": 1, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "title": "UPDATED", "body": "NEW BODY", "user_id": 1, "modifier_id": null, "creator_id": null}}
{"event": 2, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "title": "UPDATED", "body": "NEW BODY", "user_id": 1}}
```

At this stage, we have a database log that records user interactions through

the REST endpoints and the Django admin panel. Using Celery with Redis as its
backend, a periodic task can be triggered to parse the database log. The parser
processes the log, summarizes the required actions (create, update, delete),
and their related data. It also creates a backup and clears the log file for
the next run.

```python
def parse_log_file():
# Code for parsing the log file and extracting changes
```

Finally, the changes are processed through a Celery task, and the appropriate
API calls are made to update the remote server (JSONPlaceholder).

```python
@celery.task()
def apply_changes():
# Code for applying the changes to JSONPlaceholder
```

All the HTTP calls are performed asynchronously, ensuring synchronization
between the databases.

---

### Drawback

While this project is just a simple implementation of my homework, it's important to be aware of the following limitations:

1. Limited Comment Manipulations: Due to the constraints of JSONPlaceHolder, any changes made to comments will be captured but ultimately ignored. The functionality to modify comments is not supported in this task.

2. Synchronization Design: Synchronizing databases solely through HTTP, as implemented in this project, is not considered a recommended approach in real-world scenarios. It is more common to employ dedicated tools like Kubernetes StatefulSets for efficient and reliable database synchronization. Synchronizing databases through web applications and HTTP can have several limitations, including:

   1. Performance Overhead: Synchronization through web applications and HTTP introduces additional layers of communication and processing. This can result in increased latency and performance overhead compared to more direct synchronization methods, especially when dealing with large volumes of data or high-frequency updates.

   2. Network Dependency: The synchronization process relies heavily on network connectivity and stability. Any network interruptions or latency can impact the synchronization performance and overall system availability. This dependency on network infrastructure introduces potential points of failure and requires robust network configurations.

   3. Limited Control and Flexibility: Synchronization through web applications and HTTP typically operates at a higher level of abstraction, often with limited control over low-level database operations. This can restrict the ability to fine-tune synchronization settings or implement custom synchronization logic, potentially limiting the system's flexibility and adaptability to specific requirements.

   4. Security Considerations: Synchronizing databases over the web introduces security considerations. It requires careful attention to authentication, encryption, and data integrity during transmission to ensure the confidentiality and integrity of synchronized data. Failure to implement proper security measures can expose sensitive data to unauthorized access or tampering.

   5. Scalability Challenges: As the volume of data and the number of concurrent users or transactions increase, synchronizing through web applications and HTTP can face scalability challenges. It may become difficult to maintain real-time synchronization, and the increased network and processing overhead can strain the system's resources, potentially leading to performance bottlenecks.

   6. Dependency on Web Application: Synchronization through web applications and HTTP relies on the availability and stability of the web application serving as the synchronization interface. Any issues with the web application, such as downtime, errors, or performance problems, can directly impact the synchronization process and the overall system's reliability.


3. Alternative Database Synchronization Design: An alternative approach for database synchronization involves adopting a Master-Worker system design. In this design, transactions occurring on the master database are recorded in a transaction log. Replica databases continuously read and apply these log entries, ensuring near real-time synchronization with the master. Although this project shares similarities with this method, it primarily focuses on the master database updating its replicas.

4. Communication Channel Limitations: Establishing additional communication channels between systems is crucial for effective synchronization. However, due to the nature of JSONPlaceHolder as a sample REST service with inherent limitations, it was not possible to establish an alternative communication channel in this implementation.

Please consider these limitations when evaluating the suitability and scalability of this project.

---

## Tests

During the implementation of the solution, the following practices were
followed to ensure testability:

1. Writing different unit tests to evaluate and validate the functionality of
   individual components.
2. Using mocking frameworks or creating manual mock objects to simulate the
   behavior of external systems, APIs, or services. In this example, the
   functionality of fetching data from JSONPlaceholder was mocked during the
   testing of the commands.
3. Performing integration tests to verify the functionality of endpoints.
   ViewSets were tested using a mock server and a test database.
4. Generating test data intelligently to cover different scenarios such as
   creating new data, updating existing data, and deleting data. Various test
   cases can be found in the test directory, including the parser tests.

By incorporating these practices, along with unittest and pytest, example unit
and integration tests were implemented to ensure the proper functionality of
the feature.

## How to run?

A Dockerized application is provided, making it easy to test and interact with
the application. To run the entire application, use `compose.dev.yml`:

```commandline
docker-compose -f compose.dev.yml up -d
```

This application contains all the requirements for a production-ready
application server. It uses NGINX as a reverse proxy and uWSGI as the web
server, along with Celery and Redis.

Additionally, you can run the tests with coverage for the solution
implementation. The test container can be executed via the command line:

```commandline
docker-compose -f compose.test.yml up --abort-on-container-exit
```

