# Distributed Systems Reading List
- URL: https://dancres.github.io/Pages/
- Added At: 2024-10-23 14:05:49
- [Link To Text](2024-10-23-distributed-systems-reading-list_raw.md)

## TL;DR
本文探讨了分布式系统的思维转变，涵盖了系统设计、延迟处理、亚马逊和谷歌的技术实践、一致性模型、理论基础、语言工具、基础设施、存储技术、Paxos及替代共识算法、八卦协议和P2P协议等内容，旨在帮助读者深入理解分布式计算的挑战与解决方案。

## Summary
1. **引言**：
   - 分布式系统的最大挑战在于思维方式的转变。
   - 本文收集了作者认为有助于推动这种转变的资料。

2. **思维启发**：
   - **系统设计反思**：
     - [Harvest, Yield and Scalable Tolerant Systems](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.33.411)：Brewer等人对CAP定理的实际应用。
     - [On Designing and Deploying Internet Scale Services](https://mvdirona.com/jrh/talksAndPapers/JamesRH_Lisa.pdf)：James Hamilton的设计与部署经验。
     - [The Perils of Good Abstractions](https://web.archive.org/web/20181006111158/http://www.addsimplicity.com/adding_simplicity_an_engi/2006/12/the_perils_of_g.html)：构建完美API/接口的困难。
     - [Chaotic Perspectives](https://web.archive.org/web/20180821164750/http://www.addsimplicity.com/adding_simplicity_an_engi/2007/05/chaotic_perspec.html)：大规模系统的不可预测性、无序性和并行性。
     - [Data on the Outside versus Data on the Inside](http://cidrdb.org/cidr2005/papers/P12.pdf)：Pat Helland的数据内外之分。
     - [Memories, Guesses and Apologies](https://channel9.msdn.com/Shows/ARCast.TV/ARCastTV-Pat-Helland-on-Memories-Guesses-and-Apologies)：Pat Helland的记忆、猜测和道歉。
     - [SOA and Newton's Universe](https://web.archive.org/web/20190719121913/https://blogs.msdn.microsoft.com/pathelland/2007/05/20/soa-and-newtons-universe/)：Pat Helland的SOA与牛顿宇宙。
     - [Building on Quicksand](https://arxiv.org/abs/0909.1788)：Pat Helland的建于流沙之上。
     - [Why Distributed Computing?](https://www.artima.com/weblogs/viewpost.jsp?thread=4247)：Jim Waldo的分布式计算原因。
     - [A Note on Distributed Computing](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.41.7628)：Waldo, Wollrath等人的分布式计算笔记。
     - [Stevey's Google Platforms Rant](https://web.archive.org/web/20190319154842/https://plus.google.com/112678702228711889851/posts/eVeouesvaVX)：Yegge的Google平台经验。

3. **延迟问题**：
   - **延迟处理**：
     - [Latency Exists, Cope!](https://web.archive.org/web/20181004043647/http://www.addsimplicity.com/adding_simplicity_an_engi/2007/02/latency_exists_.html)：应对延迟及其架构影响。
     - [Latency - the new web performance bottleneck](https://www.igvita.com/2012/07/19/latency-the-new-web-performance-bottleneck/)：延迟作为新的性能瓶颈。
     - [The Tail At Scale](https://research.google/pubs/pub40801/)：大规模系统中的延迟挑战。

4. **亚马逊**：
   - **技术与文化**：
     - [A Conversation with Werner Vogels](https://queue.acm.org/detail.cfm?id=1142065)：亚马逊服务架构转型的讨论。
     - [Discipline and Focus](https://queue.acm.org/detail.cfm?id=1388773)：亚马逊服务架构转型的进一步讨论。
     - [Vogels on Scalability](https://web.archive.org/web/20130729204944id_/http://itc.conversationsnetwork.org/shows/detail1634.html)：Vogels的可扩展性观点。
     - [SOA creates order out of chaos @ Amazon](http://searchwebservices.techtarget.com/originalContent/0,289142,sid26_gci1195702,00.html)：亚马逊的SOA实践。

5. **谷歌**：
   - **前沿技术**：
     - [MapReduce](https://research.google/pubs/pub62/)
     - [Chubby Lock Manager](https://research.google/pubs/pub27897/)
     - [Google File System](https://research.google/pubs/pub51/)
     - [BigTable](https://research.google/pubs/pub27898/)
     - [Data Management for Internet-Scale Single-Sign-On](https://www.usenix.org/legacy/event/worlds06/tech/prelim_papers/perl/perl.pdf)
     - [Dremel: Interactive Analysis of Web-Scale Datasets](https://research.google/pubs/pub36632/)
     - [Large-scale Incremental Processing Using Distributed Transactions and Notifications](https://research.google/pubs/pub36726/)
     - [Megastore: Providing Scalable, Highly Available Storage for Interactive Services](http://cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf)
     - [Spanner](https://research.google/pubs/pub39966/)
     - [Photon](https://research.google/pubs/pub41318/)
     - [Mesa: Geo-Replicated, Near Real-Time, Scalable Data Warehousing](https://research.google/pubs/pub42851/)

6. **一致性模型**：
   - **一致性权衡**：
     - [CAP Conjecture](https://web.archive.org/web/20190629112250/https://www.glassbeam.com/sites/all/themes/glassbeam/images/blog/10.1.1.67.6951.pdf)
     - [Consistency, Availability, and Convergence](https://www.cs.utexas.edu/users/dahlin/papers/cac-tr.pdf)
     - [CAP Twelve Years Later: How the "Rules" Have Changed](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed)
     - [Consistency and Availability](https://www.infoq.com/news/2008/01/consistency-vs-availability)
     - [Eventual Consistency](https://www.allthingsdistributed.com/2007/12/eventually_consistent.html)
     - [Avoiding Two-Phase Commit](https://web.archive.org/web/20180821165044/http://www.addsimplicity.com/adding_simplicity_an_engi/2006/12/avoiding_two_ph.html)
     - [2PC or not 2PC, Wherefore Art Thou XA?](https://web.archive.org/web/20180821164931/http://www.addsimplicity.com/adding_simplicity_an_engi/2006/12/2pc_or_not_2pc_.html)
     - [Life Beyond Distributed Transactions](https://docs.microsoft.com/en-us/archive/blogs/pathelland/link-to-quotlife-beyond-distributed-transactions-an-apostates-opinion)
     - [If you have too much data, then 'good enough' is good enough](https://queue.acm.org/detail.cfm?id=1988603)
     - [Starbucks doesn't do two phase commit](https://www.enterpriseintegrationpatterns.com/docs/IEEE_Software_Design_2PC.pdf)
     - [You Can't Sacrifice Partition Tolerance](https://codahale.com/you-cant-sacrifice-partition-tolerance/)
     - [Optimistic Replication](https://www.hpl.hp.com/techreports/2002/HPL-2002-33.pdf)

7. **理论基础**：
   - **重要元素**：
     - [Distributed Computing Economics](https://arxiv.org/pdf/cs/0403019.pdf)
     - [Rules of Thumb in Data Engineering](https://www.microsoft.com/en-us/research/publication/rules-of-thumb-in-data-engineering/)
     - [Fallacies of Distributed Computing](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)
     - [Impossibility of distributed consensus with one faulty process](https://doi.acm.org/10.1145/3149.214121)
     - [Unreliable Failure Detectors for Reliable Distributed Systems](https://www.cs.utexas.edu/~lorenzo/corsi/cs380d/papers/p225-chandra.pdf)
     - [Lamport Clocks](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)
     - [The Byzantine Generals Problem](https://lamport.azurewebsites.net/pubs/byz.pdf)
     - [Lazy Replication: Exploiting the Semantics of Distributed Services](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.17.469)
     - [Scalable Agreement - Towards Ordering as a Service](https://www.usenix.org/legacy/event/hotdep10/tech/full_papers/Kapritsos.pdf)
     - [Scalable Eventually Consistent Counters over Unreliable Networks](https://arxiv.org/pdf/1307.3207v1.pdf)

8. **语言与工具**：
   - **技术问题**：
     - [Programming Distributed Erlang Applications: Pitfalls and Recipes](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.137.9417&rep=rep1&type=pdf)

9. **基础设施**：
   - **时钟管理**：
     - [Principles of Robust Timing over the Internet](https://queue.acm.org/detail.cfm?id=1773943)

10. **存储**：
    - **存储技术**：
      - [Consistent Hashing and Random Trees](https://www.akamai.com/us/en/multimedia/documents/technical-publication/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf)
      - [Amazon's Dynamo Storage Service](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html)

11. **Paxos共识算法**：
    - **Paxos理解**：
      - [The Part-Time Parliament](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf)
      - [Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
      - [Paxos Made Live - An Engineering Perspective](https://static.googleusercontent.com/media/research.google.com/en/us/archive/paxos_made_live.pdf)
      - [Revisiting the Paxos Algorithm](https://groups.csail.mit.edu/tds/paxos.html)
      - [How to build a highly available system with consensus](http://bwl-website.s3-website.us-east-2.amazonaws.com/58-Consensus/Acrobat.pdf)
      - [Reconfiguring a State Machine](https://www.microsoft.com/en-us/research/publication/reconfiguring-a-state-machine/)
      - [Implementing Fault-Tolerant Services Using the State Machine Approach: a Tutorial](https://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.20.4762)

12. **其他共识论文**：
    - **替代算法**：
      - [Mencius: Building Efficient Replicated State Machines for WANs](https://www.usenix.org/legacy/event/osdi08/tech/full_papers/mao/mao_html/)
      - [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)

13. **八卦协议（流行病行为）**：
    - **协议分析**：
      - [How robust are gossip-based communication protocols?](https://infoscience.epfl.ch/record/109302?ln=en)
      - [Astrolabe: A Robust and Scalable Technology For Distributed Systems Monitoring, Management, and Data Mining](https://www.cs.cornell.edu/home/rvr/papers/astrolabe.pdf)
      - [Epidemic Computing at Cornell](https://www.allthingsdistributed.com/historical/archives/000456.html)
      - [Fighting Fire With Fire: Using Randomized Gossip To Combat Stochastic Scalability Limits](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.4000%22)
      - [Bi-Modal Multicast](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.17.7959)
      - [ACM SIGOPS Operating Systems Review - Gossip-based computer networking](https://dl.acm.org/toc/sigops/2007/41/5)
      - [SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.18.9737)

14. **P2P**：
    - **P2P协议**：
      - [Chord](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)
      - [Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
      - [Pastry](https://rowstron.azurewebsites.net/PAST/pastry.pdf)
      - [PAST](http://research.microsoft.com/en-us/um/people/antr/PAST/hotos.pdf)
      - [SCRIBE](https://rowstron.azurewebsites.net/PAST/jsac.pdf)
