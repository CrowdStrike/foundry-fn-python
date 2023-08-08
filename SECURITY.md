![CrowdStrike Falcon](/docs/asset/cs-logo.png?raw=true)

# Security Policy

This document outlines security policy and procedures for the CrowdStrike `foundry-fn-python` project.

+ [Supported Python versions](#supported-python-versions)
+ [Supported Operating Systems](#supported-operating-systems)
+ [Supported CrowdStrike regions](#supported-crowdstrike-regions)
+ [Supported foundry-fn-python versions](#supported-foundry-fn-python-versions)
+ [Reporting a potential security vulnerability](#reporting-a-potential-security-vulnerability)
+ [Disclosure and Mitigation Process](#disclosure-and-mitigation-process)

## Supported Python versions

foundry-fn-python functionality is unit tested to run under the following versions of Python.
Unit testing is performed with every pull request or commit to `main`.

| Version |                    Supported                    |
|:--------|:-----------------------------------------------:|
| \>= 3.9 | ![Yes](https://img.shields.io/badge/-YES-green) |
| <= 3.8  |   ![No](https://img.shields.io/badge/-NO-red)   |

## Supported CrowdStrike regions

foundry-fn-python is unit tested for functionality across all commercial CrowdStrike regions.

| Region |
|:-------|
| US-1   |
| US-2   |
| EU-1   |

## Supported foundry-fn-python versions

When discovered, we release security vulnerability patches for the most recent release at an accelerated cadence.

## Reporting a potential security vulnerability

We have multiple avenues to receive security-related vulnerability reports.

Please report suspected security vulnerabilities by:

+ Submitting
  a [bug](https://github.com/CrowdStrike/foundry-fn-python/issues/new?assignees=&labels=bug+%3Abug%3A&template=bug_report.md&title=%5B+BUG+%5D+...).
+ Starting a new [discussion](https://github.com/CrowdStrike/foundry-fn-python/discussions).
+ Submitting a [pull request](https://github.com/CrowdStrike/foundry-fn-python/pulls) to potentially resolve the issue. (
  New
  contributors: please review the content
  located [here](https://github.com/CrowdStrike/foundry-fn-python/blob/main/CONTRIBUTING.md).)
+ Sending an email to __foundry-fn-python@crowdstrike.com__.

## Disclosure and mitigation process

Upon receiving a security bug report, the issue will be assigned to one of the project maintainers. This person will
coordinate the related fix and release
process, involving the following steps:

+ Communicate with you to confirm we have received the report and provide you with a status update.
    - You should receive this message within 48 - 72 business hours.
+ Confirmation of the issue and a determination of affected versions.
+ An audit of the codebase to find any potentially similar problems.
+ Preparation of patches for all releases still under maintenance.
    - These patches will be submitted as a separate pull request and contain a version update.
    - This pull request will be flagged as a security fix.
    - Once merged, and after post-merge unit testing has been completed, the patch will be immediately published to both
      PyPI repositories.

---

<p align="center"><img src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/cs-logo-footer.png"><BR/><img width="300px" src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/adversary-goblin-panda.png"></P>
<h3><P align="center">WE STOP BREACHES</P></h3>
