# 回顾《Scaling Memcache at Facebook》论文 - luozhiyun`s Blog
- URL: https://www.luozhiyun.com/archives/871
- Added At: 2025-05-19 14:19:26
- [Link To Text](2025-05-19-回顾《scaling-memcache-at-facebook》论文---luozhiyun`s-blog_raw.md)

## TL;DR
本文探讨了Memcache的设计原则、缓存一致性策略、降低延迟与负载、故障处理、跨区域复制与一致性以及单服务器优化，全面提升了Memcache的性能和可靠性。

## Summary
1. **Memcache设计原则**：
   - 首先读比写多，浏览人数大于发表人数。
   - 数据源异构性要求灵活的缓存策略，存储来自不同系统的数据。

2. **缓存一致性策略**：
   - 提出四种策略：更新数据库后更新缓存、更新数据库前更新缓存、更新数据库后删除缓存、更新数据库前删除缓存。
   - 实际场景下，先更新数据库再删除缓存的策略存在不一致的可能性。

3. **Leases机制**：
   - 解决缓存一致性问题，包括陈旧写入和惊群效应。
   - 通过令牌仲裁和速率限制解决数据一致性问题。

4. **降低延迟**：
   - 并行请求和批量处理优化RTT次数。
   - 客户端-服务器通信优化，使用mcrouter桥接。
   - 使用UDP请求降低查询延迟，TCP请求保证数据一致性。

5. **滑动窗口机制**：
   - 解决Incast Congestion问题，通过调整滑动窗口大小来控制流量。

6. **降低负载**：
   - 使用Leases机制解决陈旧写入和惊群效应。
   - Memcache Pools缓存池隔离不同业务，提高缓存命中率。
   - 池内复制提高吞吐量，适用于批量读取密集型场景。

7. **Gutter机制**：
   - 临时故障接管池，防止雪崩，降低故障率。

8. **跨区域复制**：
   - 按区域部署分散负载，提高故障隔离能力。
   - 区域失效机制和区域池管理数据。

9. **冷集群预热策略**：
   - 新集群上线时，通过请求转发到已运行集群预热。

10. **跨区域一致性**：
    - 主区域处理写入，使用远程标记机制避免数据不一致。

11. **单服务器改进**：
    - 哈希表扩展、细粒度锁定、UDP端口分配、使用UDP替代TCP等优化。

12. **总结**：
    - 优化传输协议、租约机制、池化技术、处理故障、跨区域一致性、单服务器性能等方面。
