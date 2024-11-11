
def user_has_permission(self, permission: str) -> bool:
    '''
        This function determines if user has permission to interact with
        a Django user view.

        Arguments
        -----------
        permission: The permission user should have.
        
        Returns
        -------
        Returns True on the following conditions:
        - User is superuser.
        - User has the permission specified on permission argument and the account is not global superadmin.
        - User that make the request is the owner of the account.
    '''
    
    if self.request.user.is_superuser or \
        (self.request.user.has_perm(permission) and not self.get_object().is_superuser) \
        or self.request.user.id == self.get_object().id:
        return True
    
    return False