# mrproxy

### Description
mrproxy is a Mediocre Reverse Proxy. Seriously, you should never use this for anything other than development needs. I wrote this as a quick way to inject headers for authentication outside of production.

### Installation

```bash
$ pip install mrproxy
```

### Usage

Currently the only use for mrproxy is additional headers with a request.

```bash
$ mrproxy --header="X-Auth-User: gary"
```
