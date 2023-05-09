# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: ____database____ helper
# Author: m14
# Created: 2023.04.16
# Description: ____database____ helper
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.5         2023/04/16    basic build
# -----------------------------


from typing import List, Tuple


class DatabaseHelper:
    def __init__(self, db_connection):
        self.____database____ = db_connection
    
    def bag_update_records(self, records: List[Tuple]):
        """Update multiple ____database____ records in one transaction"""
        try:
            cursor = self.____database____.cursor()
            for record in records:
                cursor.execute("UPDATE table SET count = count + %s WHERE owner_id = %s AND type = %s AND item_id = %s", 
                                (record[4] if record[3] == 'add' else -record[4], record[0], record[1], record[2]))
            self.____database____.commit()
        except Exception as e:
            self.____database____.rollback()
            print(f"Failed to update ____database____: {e}")
            
    @property
    def database(self):
        return self.____database____