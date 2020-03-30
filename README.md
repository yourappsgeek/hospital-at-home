# Hospital@Home
A remote monitoring platform to keep symptomatic patients at home to save healthcare resources

[Go to the main project page](https://devpost.com/software/telemedicine-to-the-rescue)

## Inspiration
While waiting for the wave of Covid patients, Sebastian recognized that admitting symptomatic patients to the hospitals is inefficient and fills up capacities quickly, and unnecessarily. There had to be a better way to keep the not-so-heavy cases out of the hospital, but would you know they're ok? Welcome to the idea of hospital@home.

## What it does
Vision statement: We slow the transmission and save the critical hospital resources by monitoring patients at home through hospital@home, a decentralized medical monitoring system.

During a pandemic crisis, such as the Covid-19 crisis it is vital to prevent a healthcare-system-meltdown.

If not managed properly, the exponential growth of case numbers will overhelm the healthcare system, leading into the worst-case scenario of a “melt-down”.
The first goal in the pandemic is to protect and and maximize the use of core healthcare assets, staff, beds and machines. The key strategy to implement this goal therefore has to be to keep Covid-19 cases out of hospitals for as long as possible, while making sure they are safe.

## Architecture and Design

The following characteristics describe the software architecture and the software design:

Collection of data by means of a locally-deployed wearable monitor

Transmission of this health-related data by means of local desktop or mobile devices into a stream processing engine of a cloud based infrastructure. We base our proof-of-concept on the Google cloud platform, but from the technical perspective it is possible to use offerings from different cloud infrastructure providers as well.

Data ingestion is done by a Pub/Sub service and the incoming stream is processed and analysed by a DataFlow service pipeline. The processed data is stored in a BigQuery table where the web-based dashboard reads the data and visualizes them (currently in a Bokeh server). The dashboard is exposed as https services to the outside world and users securely access data and dashboards by means of a identity-aware proxy.
## UI/UX
We implemented mockups that demonstrate the interface design for these major building blocks
* Mockup for the operator's dashboard
* Mockup of the patient app
