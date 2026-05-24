Run locally (2 commands)

git clone https://github.com/ShaanAliCreates/job-board-api

cd job-board-api

docker compose up --build

- API: http://localhost:8000
- DOCS: http://localhost:8000/docs
- DB: localhost:5433 (user:postgres,db:jobboard)

requirements: DOCKER + DOCKER COMPOSE

Migartion run automatically on first start.
Data remain persistent across restart. 'docker compose down -v ' for wiping data.


# job-board-api
this repository contains my project named job board api

++++++++++++++Pagination Design+++++++++++++++++++++++++++

This api implements cursor based pagination method for job feed
('/job/cursor') instead of tradation offset method.

Why Cursor based Pagination over offset?

Problem with Offset Pagination is for page 1500 with each page contain 10 items it scan 15010 items and then it return 10. Although it seem like it's skipping the 15000 rows but internally it read 15000 and skip then to reach required 10 rows.

~Offset pagination
[]Get slow with depth
[]with insert and delete it produce inconsistent ouput like duplicated row or skip a row

~Cursor Based Pagination
[] it limit is 10 Read exactly 10+1 rows
[] Use the last fetched row as reference and further continue from that point
[] with insert and delete it produce consistent result
[] It does not slowed even with big bulky data


o Supported by the idx_jobs_created_at 
o explain analyze verified time complexity O(log n) for cursor based pagination and O(n) for offset based pagination

Trade off : It cannot jumps on particular rows so good for infinite scroll,feeds.
for admin dashboards requiring page no. so offset is appropriate

In of ('/jobs/cursor') I return{
    "items":items,
    "next_cursor":next_cursor,
    "has_more":has_more

}

