Title: Logging, the sensible defaults

URL Source: https://gerlacdt.github.io/blog/posts/logging/

Published Time: 2024-12-23T09:00:00+01:00

Markdown Content:
Logging is a major pillar for well-designed applications. It is not only a large help during development but also critical for failure analysis and debugging.

> _The most effective debugging tool is still careful thought, coupled with judiciously placed print statements._ - **Brian W. Kernighan**

Further logging is essential for observability in production. Nonetheless, I often encounter codebases with lousy logging practices. This manifests itself in useless logging missing context or in over-logging thereby bringing down the whole system. People often forget that logging is expensive. In the following I want to list the most important logging traits for modern cloud native applications.

### Good

*   logs are a stream of text formatted events, typically streamed to STDOUT
    
*   one log event corresponds to one line
    
*   use structured logging with a machine-parsable format like JSON with predefined properties like timestamp, environment, node, cluster, log level, app name, message, request-id
    
*   prefer silent logs like described in the [unix philosophy](http://www.catb.org/esr/writings/taoup/html/ch01s06.html)
    
    > Rule of Silence: When a program has nothing surprising to say, it should say nothing.
    
*   log only actionable events, see [silent logging](https://peter.bourgon.org/blog/2016/02/07/logging-v-instrumentation.html)
    
*   use log-levels appropriately
    
*   log errors with stracktrace and other context information like user-id, transaction-id, request-id. The provided context allows you to correlate logs across different systems and pinpoint issues quickly.
    
*   aggregate your logs in a central system like ElasticSearch or Datadog to enable powerful search, analysis, and anomaly detection.
    

### Bad

*   don’t log into files
*   don’t log multiple lines for one log event
*   don’t log DEBUG information in production. The sheer volume can overwhelm the system and even cripple the log indexing infrastructure.
*   don’t log sensitive data, user-related data and secrets like passwords must not be logged regardless of the log-level.
*   don’t use logs as persistent data storage, treat them as a transient stream of events with a defined retention period.

References
----------

*   [Twelve Factor App](https://12factor.net/logs)
*   [Unix Philosophy](http://www.catb.org/esr/writings/taoup/html/ch01s06.html)
*   [Logging vs instrumentation](https://peter.bourgon.org/blog/2016/02/07/logging-v-instrumentation.html)
