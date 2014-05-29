Title: Testing External APIs in Django
Date: 2014-05-21
Category: Best Practices
Tags: django, api, testing, continuous integration
Slug: testing-external-apis-in-django
Author: Matt Camilli
Description: Many apps today rely on external APIs and knowing whether they are
down or have changed is very important. This post walks you through what
I consider to be a best practice in testing these external APIs in Django.

Many apps today rely on external APIs and knowing whether they are
down or have changed is very important. This post walks you through what
I consider to be a best practice in testing these external APIs in Django.

As the feature set of TrackMaven grew, the app became increasingly dependent on
external APIs. When designing the integration of these external services it
became very clear that we needed architect the app to handle these services
being down or unreachable. The problem arose when we wrote tests for these APIs
and builds would "break" because services were unreachable. But is the build
really broken if an external service can't be hit? Sure we want to be notified
if a service is out, especially if it is for a long period of time, but that
shouldn't affect whether our build fails or succeeds. 




