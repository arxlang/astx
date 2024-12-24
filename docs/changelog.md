# Release Notes
---

# [0.17.0](https://github.com/arxlang/astx/compare/0.16.1...0.17.0) (2024-12-24)


### Bug Fixes

* Fix warnings from ReprStruct/Undefined ([#155](https://github.com/arxlang/astx/issues/155)) ([bc48b00](https://github.com/arxlang/astx/commit/bc48b007cda50dff9da0e713bb5c4c3313709383))


### Features

* add ClassDeclStmt and ClassDefStmt ([#153](https://github.com/arxlang/astx/issues/153)) ([76739a9](https://github.com/arxlang/astx/commit/76739a9e428512c45a4c4649540293de0273bbf2))
* Improve the ASTNodes type as a generic type ([#156](https://github.com/arxlang/astx/issues/156)) ([dc9e0ae](https://github.com/arxlang/astx/commit/dc9e0ae53746abcdfa5d2a9e98cbc0f84f0f9ffd))

## [0.16.1](https://github.com/arxlang/astx/compare/0.16.0...0.16.1) (2024-11-29)


### Bug Fixes

* **refactoring:** Split datatype module into types and literals packages ([#152](https://github.com/arxlang/astx/issues/152)) ([90e828f](https://github.com/arxlang/astx/commit/90e828f550bf65b2d82b189f7dba383a97609ba4))

# [0.16.0](https://github.com/arxlang/astx/compare/0.15.0...0.16.0) (2024-11-27)


### Bug Fixes

* Add missing typechecked ([#126](https://github.com/arxlang/astx/issues/126)) ([031de47](https://github.com/arxlang/astx/commit/031de472c7cd81453b3c774ca460d758baca1f78))
* change args type in FunctionCall class ([#140](https://github.com/arxlang/astx/issues/140)) ([89feb55](https://github.com/arxlang/astx/commit/89feb5507e9e50cefd9018e0de4d7ca23d8ae05d))
* Improve the usage of typechecked ([#127](https://github.com/arxlang/astx/issues/127)) ([97fb87c](https://github.com/arxlang/astx/commit/97fb87cb3901e5e3974c86b6265a0b3be06b33b8))


### Features

* `ImportExpr` and `ImportFromExpr` ([#122](https://github.com/arxlang/astx/issues/122)) ([7785ba7](https://github.com/arxlang/astx/commit/7785ba7198fb55aecb2a68e856308c72028a702c))
* add `IfExpr` class ([#143](https://github.com/arxlang/astx/issues/143)) ([4301e2a](https://github.com/arxlang/astx/commit/4301e2a05178f61d73336c9dcd78e71ed2024dc6))
* add ForCountLoopExpr class ([#141](https://github.com/arxlang/astx/issues/141)) ([0bdebdd](https://github.com/arxlang/astx/commit/0bdebdd98bad723eb09738d7bc566dba4a517938))
* Add Python Transpiler ([#115](https://github.com/arxlang/astx/issues/115)) ([225f398](https://github.com/arxlang/astx/commit/225f398fc860b23af7bc3e8db4925f46b67ff47c))
* Add support for char and string ([#125](https://github.com/arxlang/astx/issues/125)) ([7b8f52d](https://github.com/arxlang/astx/commit/7b8f52dd5ea9601f743e7fc3b445741bc4a99445))
* Add support for complex32 and complex64 ([#124](https://github.com/arxlang/astx/issues/124)) ([d9df755](https://github.com/arxlang/astx/commit/d9df755e3bb0cc6ae9378647c47f230c066e6b91))
* Add support for date, time, datetime, timestamp ([#146](https://github.com/arxlang/astx/issues/146)) ([e5ffb9b](https://github.com/arxlang/astx/commit/e5ffb9b4e5283103178f3b7104ab56364e6fd96e))
* Add support for ForRangeLoopExpr ([#133](https://github.com/arxlang/astx/issues/133)) ([5fb1805](https://github.com/arxlang/astx/commit/5fb1805c924a147a0fc3e648d0db6c2588d23d33))
* Add support for LambdaExpr ([#123](https://github.com/arxlang/astx/issues/123)) ([3ec145f](https://github.com/arxlang/astx/commit/3ec145fe28f006a89703a609df9d2a7287cb3c9a))
* Add support for WhileExpr class ([#142](https://github.com/arxlang/astx/issues/142)) ([e94ca1a](https://github.com/arxlang/astx/commit/e94ca1ac481abd723b7759faa44b0ba13b4c881e))
* Add support to `Import`, and `ImportFrom` statement and `Alias` expression  ([#118](https://github.com/arxlang/astx/issues/118)) ([617f506](https://github.com/arxlang/astx/commit/617f5064645f0121e4f41e3ce6a26349acc360b9))
* add TypeCastExpr class ([#130](https://github.com/arxlang/astx/issues/130)) ([3a18439](https://github.com/arxlang/astx/commit/3a184396244100ade955e3d40d5f46d40bfc2fdd))
* Implement runtime type checking with typeguard ([#119](https://github.com/arxlang/astx/issues/119)) ([b03014e](https://github.com/arxlang/astx/commit/b03014eac9cb571346545c5557408fdc130ac614))
* **transpiler:** Add support for bool operators ([#137](https://github.com/arxlang/astx/issues/137)) ([18a0e2f](https://github.com/arxlang/astx/commit/18a0e2f1093610a90fd5926f776d39d00d691cb7))

# [0.15.0](https://github.com/arxlang/astx/compare/0.14.0...0.15.0) (2024-09-14)


### Features

* Add Support for Float Datatypes (float16, float32, float64) ([#86](https://github.com/arxlang/astx/issues/86)) ([2e48959](https://github.com/arxlang/astx/commit/2e48959725535e9c7aed978199e57feff04ec0a0))

# [0.14.0](https://github.com/arxlang/astx/compare/0.13.2...0.14.0) (2024-09-09)


### Features

* Add support for int128 ([#76](https://github.com/arxlang/astx/issues/76)) ([9dfe465](https://github.com/arxlang/astx/commit/9dfe465eb4b8f53e6cab4be89e41cf8e03045a33))
* Add support for Unsigned Integers datatypes uint8, uint16, unit32, uint64, uint 128 ([#81](https://github.com/arxlang/astx/issues/81)) ([5a72f95](https://github.com/arxlang/astx/commit/5a72f958b0889fdf60b8b89d6202e99afd085c2c))

## [0.13.2](https://github.com/arxlang/astx/compare/0.13.1...0.13.2) (2024-07-26)


### Bug Fixes

* Fix FOR-LOOPs AST structure output ([#72](https://github.com/arxlang/astx/issues/72)) ([8cbb104](https://github.com/arxlang/astx/commit/8cbb1048d8c9eef5e74042f316c1ab0588935c74))

## [0.13.1](https://github.com/arxlang/astx/compare/0.13.0...0.13.1) (2024-07-26)


### Bug Fixes

* Fix graphviz diagram ([#68](https://github.com/arxlang/astx/issues/68)) ([97fb871](https://github.com/arxlang/astx/commit/97fb8718a7a734193c541e5ac3606ed39f4d5881))
* Fix IF and FUNCTION-CALL AST struct representation ([#71](https://github.com/arxlang/astx/issues/71)) ([87fffbe](https://github.com/arxlang/astx/commit/87fffbe570271563dddfe1e50322d92a15026c05))

# [0.13.0](https://github.com/arxlang/astx/compare/0.12.3...0.13.0) (2024-06-03)


### Bug Fixes

* set ReprStruct as ast data type in funcs ([#66](https://github.com/arxlang/astx/issues/66)) ([5ac2e73](https://github.com/arxlang/astx/commit/5ac2e739e3f5913843f22075321602b7ce53001d))


### Features

* add ascii repr in the console ([#52](https://github.com/arxlang/astx/issues/52)) ([71a9039](https://github.com/arxlang/astx/commit/71a9039795062ac4fb9267b1ce64b41a042549ca))
* Improve FunctionCall and add support for While AST statement ([#65](https://github.com/arxlang/astx/issues/65)) ([c4adea5](https://github.com/arxlang/astx/commit/c4adea571cdea84b9138f900abb10407a639b806))

## [0.12.3](https://github.com/arxlang/astx/compare/0.12.2...0.12.3) (2024-05-02)


### Bug Fixes

* Test coverage for more than 95% of the code and fix general issues ([#64](https://github.com/arxlang/astx/issues/64)) ([13d5d3c](https://github.com/arxlang/astx/commit/13d5d3c1c1f52dd8cad902a0120be2495fa6ce38))

## [0.12.2](https://github.com/arxlang/astx/compare/0.12.1...0.12.2) (2024-05-02)


### Bug Fixes

* Support subscripting to get nodes by index ([#63](https://github.com/arxlang/astx/issues/63)) ([102bf75](https://github.com/arxlang/astx/commit/102bf75f2eeeadd153b1381e134423a747534638))

## [0.12.1](https://github.com/arxlang/astx/compare/0.12.0...0.12.1) (2024-05-02)


### Bug Fixes

* Fix the usage of Function Arguments ([#62](https://github.com/arxlang/astx/issues/62)) ([6c78b66](https://github.com/arxlang/astx/commit/6c78b6684c8dae7b4b6a012049f8046fc3968066))

# [0.12.0](https://github.com/arxlang/astx/compare/0.11.0...0.12.0) (2024-04-28)


### Features

* Add initial support for context (parent node) ([#61](https://github.com/arxlang/astx/issues/61)) ([f1200a7](https://github.com/arxlang/astx/commit/f1200a7b9dece7f61b411d6a4655b3f79fed0b82))

# [0.11.0](https://github.com/arxlang/astx/compare/0.10.0...0.11.0) (2024-04-21)


### Features

* Add AST for Program, Package, and Target ([#58](https://github.com/arxlang/astx/issues/58)) ([87865a8](https://github.com/arxlang/astx/commit/87865a887bd515a4b7c3a65680f1e4f4b2c4367f))

# [0.10.0](https://github.com/arxlang/astx/compare/0.9.1...0.10.0) (2024-04-19)


### Bug Fixes

* Fix get_struct for variables ([#59](https://github.com/arxlang/astx/issues/59)) ([7f4ec89](https://github.com/arxlang/astx/commit/7f4ec8917ab8c814af8d4730e48e9c517c65d3bd))


### Features

* Add structure for the output from asciinet approach ([#55](https://github.com/arxlang/astx/issues/55)) ([f66beb5](https://github.com/arxlang/astx/commit/f66beb5d00b58b75978e6b64427955d5a02bdc8f))

## [0.9.1](https://github.com/arxlang/astx/compare/0.9.0...0.9.1) (2024-03-23)


### Bug Fixes

* **docs:** Fix contributing guide and getting started tutorial ([#53](https://github.com/arxlang/astx/issues/53)) ([e51d83f](https://github.com/arxlang/astx/commit/e51d83f970895188868d025768229bc9e3b0696f))

# [0.9.0](https://github.com/arxlang/astx/compare/0.8.0...0.9.0) (2024-03-06)


### Features

* create LiteralBoolean class ([#51](https://github.com/arxlang/astx/issues/51)) ([5b84b04](https://github.com/arxlang/astx/commit/5b84b04fe047e556a3446e380032a88d650a0013))
* Improve DataTypeOp and add Tutorial about For Loops ([#29](https://github.com/arxlang/astx/issues/29)) ([195c57b](https://github.com/arxlang/astx/commit/195c57bf969da2a653887bc9beddbfe89772eab9))
* Improve Function classes and add a tutorial about that ([#27](https://github.com/arxlang/astx/issues/27)) ([f8608d5](https://github.com/arxlang/astx/commit/f8608d54946cd6b452369eae2991856054482fca))
* Improve Variables classes ([#26](https://github.com/arxlang/astx/issues/26)) ([d981f88](https://github.com/arxlang/astx/commit/d981f88ef4d8f9ca77e5f6d2290e10b8149bd2dc))

# [0.8.0](https://github.com/arxlang/astx/compare/0.7.1...0.8.0) (2024-01-08)


### Features

* Add new data types for LiteralInt8, LiteralInt16, LiteralIn64 ([#24](https://github.com/arxlang/astx/issues/24)) ([40230ec](https://github.com/arxlang/astx/commit/40230ec72d447b0aa31012e1c0d81cdc37b0c34b))

## [0.7.1](https://github.com/arxlang/astx/compare/0.7.0...0.7.1) (2023-12-05)


### Bug Fixes

* Fix typing issues ([#19](https://github.com/arxlang/astx/issues/19)) ([9cb53c4](https://github.com/arxlang/astx/commit/9cb53c46f05db17f36af0d412527c56ceef922b0))

# [0.7.0](https://github.com/arxlang/astx/compare/0.6.0...0.7.0) (2023-12-05)


### Features

* Add ref attribute to the Expr class ([#18](https://github.com/arxlang/astx/issues/18)) ([60b9b0e](https://github.com/arxlang/astx/commit/60b9b0e08d0690595517a3e1659b04f5434e14c4))

# [0.6.0](https://github.com/arxlang/astx/compare/0.5.1...0.6.0) (2023-09-07)


### Features

* Add options for the graph visualization objects shape ([#16](https://github.com/arxlang/astx/issues/16)) ([93f6ebd](https://github.com/arxlang/astx/commit/93f6ebd2cec7fee718ee37e5fb6e982cdd97fbc6))

## [0.5.1](https://github.com/arxlang/astx/compare/0.5.0...0.5.1) (2023-09-07)


### Bug Fixes

* Fix docs generation ([#15](https://github.com/arxlang/astx/issues/15)) ([e1bfb4e](https://github.com/arxlang/astx/commit/e1bfb4e0447798d468a249183e35922581a8d197))

# [0.5.0](https://github.com/arxlang/astx/compare/0.4.0...0.5.0) (2023-09-06)


### Features

* Add initial support for jupyter display with graphviz ([#14](https://github.com/arxlang/astx/issues/14)) ([35a8c98](https://github.com/arxlang/astx/commit/35a8c98b328b94fd279df0711cea102dc6e8f536))

# [0.4.0](https://github.com/arxlang/astx/compare/0.3.3...0.4.0) (2023-09-05)


### Features

* Represent the ASTx in `yaml` and `json` formats ([#13](https://github.com/arxlang/astx/issues/13)) ([26d22af](https://github.com/arxlang/astx/commit/26d22af8c07988dccecf763b51d63c26394c1412))

## [0.3.3](https://github.com/arxlang/astx/compare/0.3.2...0.3.3) (2023-08-30)


### Bug Fixes

* **config:** Fix configuration and improve documentation ([#12](https://github.com/arxlang/astx/issues/12)) ([fbb8898](https://github.com/arxlang/astx/commit/fbb88984c1f208177eefd0c3d45fbab1cae012d9))

## [0.3.2](https://github.com/arxlang/astx/compare/0.3.1...0.3.2) (2023-08-22)


### Bug Fixes

* Fix logo in the documentation and fix configuration files style. ([#11](https://github.com/arxlang/astx/issues/11)) ([8552e08](https://github.com/arxlang/astx/commit/8552e08d5f2c3528dac9bc735caa8abf8f1d1ca4))

## [0.3.1](https://github.com/arxlang/astx/compare/0.3.0...0.3.1) (2023-08-22)


### Bug Fixes

* fix documentation release workflow ([#10](https://github.com/arxlang/astx/issues/10)) ([6cfb9a6](https://github.com/arxlang/astx/commit/6cfb9a663c63e80a2d8bb251439f1b32b516de42))

# [0.3.0](https://github.com/arxlang/astx/compare/0.2.1...0.3.0) (2023-08-22)


### Bug Fixes

* Fix the current linter configuration and the dependencies' pinning ([#9](https://github.com/arxlang/astx/issues/9)) ([d310511](https://github.com/arxlang/astx/commit/d3105113250cd866c3b679710d5fb1f106a0d597))


### Features

* Add support for ForRangeLoop and ForCountLoop ([#7](https://github.com/arxlang/astx/issues/7)) ([bb77de1](https://github.com/arxlang/astx/commit/bb77de1faa283e0b2aa49e84615050b59c56ab09))

## [0.2.1](https://github.com/arxlang/astx/compare/0.2.0...0.2.1) (2023-08-07)


### Bug Fixes

* Refactor Control flow classes and improve Documentation ([#6](https://github.com/arxlang/astx/issues/6)) ([4013398](https://github.com/arxlang/astx/commit/40133989f7af3cfdf6ced941d0c59184866ee850))

# [0.2.0](https://github.com/arxlang/astx/compare/0.1.1...0.2.0) (2023-08-07)


### Bug Fixes

* Fix release configuration ([#5](https://github.com/arxlang/astx/issues/5)) ([13cd6e1](https://github.com/arxlang/astx/commit/13cd6e126c6edec9f6bf935891cb7271fdafb2c3))


### Features

* Overload DataType operators ([#4](https://github.com/arxlang/astx/issues/4)) ([3b93128](https://github.com/arxlang/astx/commit/3b93128cbe42390680152de96b161f483ecef891))
