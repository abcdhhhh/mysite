class router:
    def db_for_read(self, model, **hints):
        """
        Reads go to read_db
        """
        return 'read_db'

    def db_for_write(self, model, **hints):
        """
        Writes go to write_db
        """
        return 'write_db'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the read/write pool.
        """
        # db_set = {'read', 'write'}
        # if obj1._state.db in db_set and obj2._state.db in db_set:
        return True
        # return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
