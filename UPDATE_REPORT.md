## Dependency Updates

### Summary
- Update type: minor
- Date: Mon Jul 14 09:36:02 UTC 2025
- Triggered by: schedule

### Changes
```
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
47c47
< version = "1.8.5"
---
> version = "1.8.6"
55c55
< sdist = { url = "https://files.pythonhosted.org/packages/4e/01/b2ce2f54db060ed7b25960892b275ad8238ca15f5a8821b09f8e7f75870d/bandit-1.8.5.tar.gz", hash = "sha256:db812e9c39b8868c0fed5278b77fffbbaba828b4891bc80e34b9c50373201cfd", size = 4237566, upload-time = "2025-06-17T01:43:36.697Z" }
---
> sdist = { url = "https://files.pythonhosted.org/packages/fb/b5/7eb834e213d6f73aace21938e5e90425c92e5f42abafaf8a6d5d21beed51/bandit-1.8.6.tar.gz", hash = "sha256:dbfe9c25fc6961c2078593de55fd19f2559f9e45b99f1272341f5b95dea4e56b", size = 4240271, upload-time = "2025-07-06T03:10:50.9Z" }
57c57
<     { url = "https://files.pythonhosted.org/packages/02/b0/5c8976e61944f91904d4fd33bdbe55248138bfbd1a6092753b1b0fb7abbc/bandit-1.8.5-py3-none-any.whl", hash = "sha256:cb2e57524e99e33ced48833c6cc9c12ac78ae970bb6a450a83c4b506ecc1e2f9", size = 131759, upload-time = "2025-06-17T01:43:35.045Z" },
---
>     { url = "https://files.pythonhosted.org/packages/48/ca/ba5f909b40ea12ec542d5d7bdd13ee31c4d65f3beed20211ef81c18fa1f3/bandit-1.8.6-py3-none-any.whl", hash = "sha256:3348e934d736fcdb68b6aa4030487097e23a501adf3e7827b63658df464dddd0", size = 133808, upload-time = "2025-07-06T03:10:49.134Z" },
78c78
< version = "2025.6.15"
---
> version = "2025.7.14"
80c80
< sdist = { url = "https://files.pythonhosted.org/packages/73/f7/f14b46d4bcd21092d7d3ccef689615220d8a08fb25e564b65d20738e672e/certifi-2025.6.15.tar.gz", hash = "sha256:d747aa5a8b9bbbb1bb8c22bb13e22bd1f18e9796defa16bab421f7f7a317323b", size = 158753, upload-time = "2025-06-15T02:45:51.329Z" }
---
> sdist = { url = "https://files.pythonhosted.org/packages/b3/76/52c535bcebe74590f296d6c77c86dabf761c41980e1347a2422e4aa2ae41/certifi-2025.7.14.tar.gz", hash = "sha256:8ea99dbdfaaf2ba2f9bac77b9249ef62ec5218e7c2b2e903378ed5fccf765995", size = 163981, upload-time = "2025-07-14T03:29:28.449Z" }
82c82
<     { url = "https://files.pythonhosted.org/packages/84/ae/320161bd181fc06471eed047ecce67b693fd7515b16d495d8932db763426/certifi-2025.6.15-py3-none-any.whl", hash = "sha256:2e0c7ce7cb5d8f8634ca55d2ba7e6ec2689a2fd6537d8dec1296a477a4910057", size = 157650, upload-time = "2025-06-15T02:45:49.977Z" },
---
>     { url = "https://files.pythonhosted.org/packages/4f/52/34c6cf5bb9285074dc3531c437b3919e825d976fde097a7a73f79e726d03/certifi-2025.7.14-py3-none-any.whl", hash = "sha256:6b31f564a415d79ee77df69d757bb49a5bb53bd9f756cbbe24394ffd6fc1f4b2", size = 162722, upload-time = "2025-07-14T03:29:26.863Z" },
346c346
<     { name = "typing-extensions", marker = "python_full_version < '3.11'" },
---
>     { name = "typing-extensions", marker = "python_full_version < '3.13'" },
373c373
< version = "6.135.24"
---
> version = "6.135.29"
380c380
< sdist = { url = "https://files.pythonhosted.org/packages/cf/ae/f846b67ce9fc80cf51cece6b7adaa3fe2de4251242d142e241ce5d4aa26f/hypothesis-6.135.24.tar.gz", hash = "sha256:e301aeb2691ec0a1f62bfc405eaa966055d603e328cd854c1ed59e1728e35ab6", size = 454011, upload-time = "2025-07-03T02:46:51.776Z" }
---
> sdist = { url = "https://files.pythonhosted.org/packages/19/5e/0313a89bae4bc6b28dc4afcc72e9ee0fe15c86ead45b4ea14996c7a85ea9/hypothesis-6.135.29.tar.gz", hash = "sha256:871acb38ff61346a420267f81f4ba05ad9a85d08965211edf9b29bc0c1ad9d7b", size = 455112, upload-time = "2025-07-12T18:18:00.125Z" }
382c382
<     { url = "https://files.pythonhosted.org/packages/ed/cb/c38acf27826a96712302229622f32dd356b9c4fbe52a3e9f615706027af8/hypothesis-6.135.24-py3-none-any.whl", hash = "sha256:88ed21fbfa481ca9851a9080841b3caca14cd4ed51a165dfae8006325775ee72", size = 520920, upload-time = "2025-07-03T02:46:48.286Z" },
```

### Test Results
✅ All tests passed after dependency update

### Next Steps
1. Review the changes in this PR
2. Test the application manually if needed
3. Merge if everything looks good
