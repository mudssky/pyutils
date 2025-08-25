## Dependency Updates

### Summary
- Update type: minor
- Date: Mon Aug 25 09:29:31 UTC 2025
- Triggered by: schedule

### Changes
```
2c2
< revision = 2
---
> revision = 3
20c20
< version = "22.2.0"
---
> version = "25.3.0"
22c22
< sdist = { url = "https://files.pythonhosted.org/packages/21/31/3f468da74c7de4fcf9b25591e682856389b3400b4b62f201e65f15ea3e07/attrs-22.2.0.tar.gz", hash = "sha256:c9227bfc2f01993c03f68db37d1d15c9690188323c067c641f1a35ca58185f99", size = 215900, upload-time = "2022-12-21T09:48:51.773Z" }
---
> sdist = { url = "https://files.pythonhosted.org/packages/5a/b0/1367933a8532ee6ff8d63537de4f1177af4bff9f3e829baf7331f595bb24/attrs-25.3.0.tar.gz", hash = "sha256:75d7cefc7fb576747b2c81b4442d4d4a1ce0900973527c011d1030fd3bf4af1b", size = 812032, upload-time = "2025-03-13T11:10:22.779Z" }
24c24
<     { url = "https://files.pythonhosted.org/packages/fb/6e/6f83bf616d2becdf333a1640f1d463fef3150e2e926b7010cb0f81c95e88/attrs-22.2.0-py3-none-any.whl", hash = "sha256:29e95c7f6778868dbd49170f98f8818f78f3dc5e0e37c0b1f474e3561b240836", size = 60018, upload-time = "2022-12-21T09:48:49.401Z" },
---
>     { url = "https://files.pythonhosted.org/packages/77/06/bb80f5f86020c4551da315d78b3ab75e8228f89f0162f2c3a819e407941a/attrs-25.3.0-py3-none-any.whl", hash = "sha256:427318ce031701fea540783410126f03899a97ffc6f61596ad581ac2e40e3bc3", size = 63815, upload-time = "2025-03-13T11:10:21.14Z" },
36a37,45
> name = "backports-asyncio-runner"
> version = "1.2.0"
> source = { registry = "https://pypi.org/simple" }
> sdist = { url = "https://files.pythonhosted.org/packages/8e/ff/70dca7d7cb1cbc0edb2c6cc0c38b65cba36cccc491eca64cabd5fe7f8670/backports_asyncio_runner-1.2.0.tar.gz", hash = "sha256:a5aa7b2b7d8f8bfcaa2b57313f70792df84e32a2a746f585213373f900b42162", size = 69893, upload-time = "2025-07-02T02:27:15.685Z" }
> wheels = [
>     { url = "https://files.pythonhosted.org/packages/a0/59/76ab57e3fe74484f48a53f8e337171b4a2349e506eabe136d7e01d059086/backports_asyncio_runner-1.2.0-py3-none-any.whl", hash = "sha256:0da0a936a8aeb554eccb426dc55af3ba63bcdc69fa1a600b5bb305413a4477b5", size = 12313, upload-time = "2025-07-02T02:27:14.263Z" },
> ]
> 
> [[package]]
47c56
< version = "1.8.5"
---
> version = "1.8.6"
55c64
< sdist = { url = "https://files.pythonhosted.org/packages/4e/01/b2ce2f54db060ed7b25960892b275ad8238ca15f5a8821b09f8e7f75870d/bandit-1.8.5.tar.gz", hash = "sha256:db812e9c39b8868c0fed5278b77fffbbaba828b4891bc80e34b9c50373201cfd", size = 4237566, upload-time = "2025-06-17T01:43:36.697Z" }
---
> sdist = { url = "https://files.pythonhosted.org/packages/fb/b5/7eb834e213d6f73aace21938e5e90425c92e5f42abafaf8a6d5d21beed51/bandit-1.8.6.tar.gz", hash = "sha256:dbfe9c25fc6961c2078593de55fd19f2559f9e45b99f1272341f5b95dea4e56b", size = 4240271, upload-time = "2025-07-06T03:10:50.9Z" }
57c66
<     { url = "https://files.pythonhosted.org/packages/02/b0/5c8976e61944f91904d4fd33bdbe55248138bfbd1a6092753b1b0fb7abbc/bandit-1.8.5-py3-none-any.whl", hash = "sha256:cb2e57524e99e33ced48833c6cc9c12ac78ae970bb6a450a83c4b506ecc1e2f9", size = 131759, upload-time = "2025-06-17T01:43:35.045Z" },
---
>     { url = "https://files.pythonhosted.org/packages/48/ca/ba5f909b40ea12ec542d5d7bdd13ee31c4d65f3beed20211ef81c18fa1f3/bandit-1.8.6-py3-none-any.whl", hash = "sha256:3348e934d736fcdb68b6aa4030487097e23a501adf3e7827b63658df464dddd0", size = 133808, upload-time = "2025-07-06T03:10:49.134Z" },
62c71
< version = "1.2.2.post1"
---
> version = "1.3.0"
71c80
< sdist = { url = "https://files.pythonhosted.org/packages/7d/46/aeab111f8e06793e4f0e421fcad593d547fb8313b50990f31681ee2fb1ad/build-1.2.2.post1.tar.gz", hash = "sha256:b36993e92ca9375a219c99e606a122ff365a760a2d4bba0caa09bd5278b608b7", size = 46701, upload-time = "2024-10-06T17:22:25.251Z" }
---
> sdist = { url = "https://files.pythonhosted.org/packages/25/1c/23e33405a7c9eac261dff640926b8b5adaed6a6eb3e1767d441ed611d0c0/build-1.3.0.tar.gz", hash = "sha256:698edd0ea270bde950f53aed21f3a0135672206f3911e0176261a31e0e07b397", size = 48544, upload-time = "2025-08-01T21:27:09.268Z" }
73c82
<     { url = "https://files.pythonhosted.org/packages/84/c2/80633736cd183ee4a62107413def345f7e6e3c01563dbca1417363cf957e/build-1.2.2.post1-py3-none-any.whl", hash = "sha256:1d61c0887fa860c01971625baae8bdd338e517b836a2f70dd1f7aa3a6b2fc5b5", size = 22950, upload-time = "2024-10-06T17:22:23.299Z" },
---
>     { url = "https://files.pythonhosted.org/packages/cb/8c/2b30c12155ad8de0cf641d76a8b396a16d2c36bc6d50b621a62b7c4567c1/build-1.3.0-py3-none-any.whl", hash = "sha256:7145f0b5061ba90a1500d60bd1b13ca0a8a4cebdd0cc16ed8adf1c0e739f43b4", size = 23382, upload-time = "2025-08-01T21:27:07.844Z" },
```

### Test Results
✅ All tests passed after dependency update

### Next Steps
1. Review the changes in this PR
2. Test the application manually if needed
3. Merge if everything looks good
