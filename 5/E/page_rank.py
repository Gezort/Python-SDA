def PR(graph, damping_factor=0, eps=0.0001):
    pr = dict()
    n_urls = len(graph)
    for url in graph:
        pr[url] = 1. / n_urls
    diff = eps * 10
    while diff > eps:
        new_pr = dict()
        for url in graph:
            new_pr[url] = damping_factor / n_urls
        for url in graph:
            n_children = len(graph[url])
            if n_children > 0:
                for child in graph[url]:
                    new_pr[child] += (1 - damping_factor) * pr[
                            url] / n_children
            else:
                new_pr[url] += (1 - damping_factor) * pr[url]
        diff = 0
        for url in graph:
            diff += abs(new_pr[url] - pr[url])
        pr = new_pr.copy()
    return pr
