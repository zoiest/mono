# Elements of Programming Interviews (Exercises)

This project uses [Bazel](https://bazel.build) to build and test programming exercises in both **C++** and **Go**.

## Project Structure

```
gym/elems/
├── MODULE.bazel
├── BUILD.bazel
├── .bazelrc
└── 00_00_sample_parity/
    ├── cpp/
    │   ├── parity.h
    │   ├── parity.cc
    │   ├── parity_test.cc
    │   └── BUILD.bazel
    └── go/
        ├── parity.go
        ├── parity_test.go
        └── BUILD.bazel
```

## Running Tests

Run all tests (both C++ and Go):
```bash
bazel test //...
```

Run tests for a specific package:
```bash
# C++ test
bazel test //00_00_sample_parity/cpp:parity_test

# Go test
bazel test //00_00_sample_parity/go:parity_test
```

## Adding a New Exercise

### C++ Exercise
Create a directory with `BUILD.bazel`:
```starlark
cc_library(
    name = "solution",
    srcs = ["solution.cc"],
    hdrs = ["solution.h"],
)

cc_test(
    name = "solution_test",
    srcs = ["solution_test.cc"],
    deps = [":solution"],
)
```

### Go Exercise
Create a directory with `BUILD.bazel`:
```starlark
load("@rules_go//go:def.bzl", "go_library", "go_test")

go_library(
    name = "solution",
    srcs = ["solution.go"],
    importpath = "github.com/zoiest/mono/gym/elems/your_exercise/go",
)

go_test(
    name = "solution_test",
    srcs = ["solution_test.go"],
    embed = [":solution"],
)
```

Or run Gazelle to generate Go `BUILD` files automatically:
```bash
bazel run //:gazelle
```
