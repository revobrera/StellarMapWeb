const lineage_table_mixin = {
    data() {
      return {
        transProps: {
          // Transition name
          name: 'flip-list'
        },
        items: [
          { Active: 'Account (active)', Created: '05/06/2021', Account: 'YUIB' },
          { Active: 'Account (active)', Created: '06/03/2021', Account: 'UIBC' },
          { Active: 'Account (active)', Created: '06/17/2021', Account: 'OPIU' },
          { Active: 'Account (disabled)', Created: '07/17/2021', Account: 'MNUB' }
        ],
        fields: [
          { key: 'Active', sortable: true },
          { key: 'Created', sortable: true },
          { key: 'Account', sortable: true },
          { key: 'Home Domain', sortable: true },
          { key: 'XLM Balance', sortable: true },
          { key: 'Stellar.Expert', sortable: true }
        ]
      }
    }
  }

  