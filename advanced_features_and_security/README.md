## Permissions and Groups Setup

I added four custom permissions to `Book`:

- `can_view`  
- `can_create`  
- `can_edit`  
- `can_delete`  

Three groups manage these:

| Group   | Permissions                      |
| ------- | -------------------------------- |
| Viewers | can_view                         |
| Editors | can_view, can_create, can_edit   |
| Admins  | can_view, can_create, can_edit, can_delete |

Views are protected with:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
