# Library Management System

A custom [Frappe Framework](https://frappeframework.com) application for managing a library's books, members, and lending workflow — built as a hands-on learning project.

## Overview

This app models a simple library's day-to-day operations:

- Maintaining a catalog of articles (books)
- Registering and managing library members
- Issuing memberships with automatic expiry calculation
- Issuing and returning books with built-in business rules
- Daily background checks via a scheduled task

## Features

### DocTypes

| DocType | Description |
|---|---|
| **Article** | Represents a book in the library catalog (title, author, ISBN, status, etc.) |
| **Library Member** | Represents a registered library member |
| **Library Membership** | Tracks a member's active membership period |
| **Library Transaction** | Records book issue/return events |

### Business Logic

- **Membership validation** — a member cannot have two overlapping active memberships
- **Automatic membership expiry** — `to_date` is calculated from `from_date` + configurable loan period
- **Issue validation** — a book cannot be issued if it's already issued to someone else
- **Membership check on issue** — a book can only be issued to a member with a valid, active membership
- **Borrowing limit** — a member cannot exceed the maximum number of books allowed at once (configurable)
- **Return validation** — a book cannot be returned unless it was issued first

### Automation

- A daily scheduled task (`scheduler_events`) checks library transactions in the background — no manual action required from the user.

## Settings

Configuration is managed through a **Library Settings** singleton DocType:

- `loan_period` — number of days a membership remains valid
- `max_articles` — maximum number of books a member can have issued at once

## Installation

This app is built on the [Frappe Framework](https://frappeframework.com) and requires a working Frappe bench.

```bash
# From your frappe-bench directory
bench get-app https://github.com/MuneebIftkhar119/Library-Management.git
bench --site your-site-name install-app library_management
```

## Tech Stack

- **Framework:** Frappe (Python + JavaScript)
- **Database:** MariaDB
- **Backend:** Python controllers using Frappe's Document hooks (`validate`, `before_submit`, `on_submit`)

## Project Structure

```
library_management/
├── library_managment/
│   └── doctype/
│       ├── article/
│       ├── library_member/
│       ├── library_membership/
│       └── library_transaction/
├── tasks.py          # Scheduled background jobs
└── hooks.py           # App configuration & event hooks
```

## Author

**Muneeb Iftikhar**
📧 officialmunneb@gmail.com

## License

MIT
