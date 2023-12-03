const lineage_table_mixin = {
    data() {
      return {
        transProps: {
          // Transition name
          name: 'flip-list',
          account_genealogy_items: {
            type: [Array, Function],
            required: true
          }
        },
        account_genealogy_items: [],
        account_genealogy_fields: [
          { key: 'index', label: 'Index', sortable: true, visible: true },
          { key: 'stellar_creator_account', label: 'Creator Account', sortable: true, visible: false },
          { key: 'stellar_account_created_at', label: 'Account Created At', sortable: true, visible: true },
          { key: 'stellar_account', label: 'Account', sortable: true, visible: true },
          { key: 'network_name', label: 'Network Name', sortable: true, visible: true },
          { key: 'home_domain', label: 'Home Domain', sortable: true, visible: true },
          { key: 'xlm_balance', label: 'XLM Balance', sortable: true, visible: true },
          { key: 'stellar_expert', label: 'Stellar Expert', sortable: true, visible: true },
          { key: 'status', label: 'Status', sortable: true, visible: true },
          { key: 'updated_at', label: 'Updated At', sortable: true, visible: true }
        ],
        apiStellarExpertTagsResponses: [],
        tree_genealogy_items: null,
        // StellarMap Radial Tree or SMRT
        smrt_treeGenealogyItems: null,
        smrt_tooltip: null,
        smrt_navbars: null,
        smrt_diameter: 570,
        smrt_width: null,
        smrt_height: null,
        smrt_counter: 0,
        smrt_duration: 350,
        smrt_root: null,
        smrt_tree: null,
        smrt_filteredPartition: null,
        smrt_radialProjection: null,
        smrt_svg: null,
        smrt_color: null,
        smrt_legend: null,
        smrt_angle: 0,
        smrt_buttons: null
      }
    },
    mounted() {
      this.smrt_treeGenealogyItems = "{{ tree_genealogy_items }}";
      this.smrt_tooltip = d3.select('#display_radial_tidy_tree')
        .append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .style('left', 0)
        .style('top', 0);
      this.smrt_navbars = d3.select('div.b')
        .append('nav')
        .attr('class', 'breadcrumbs');
      this.smrt_width = this.smrt_diameter;
      this.smrt_height = this.smrt_diameter;
      this.smrt_root = this.smrt_treeGenealogyItems;
      this.smrt_root.x0 = this.smrt_height / 2;
      this.smrt_root.y0 = 0;
      this.smrt_tree = d3.layout.tree()
        .size([360, this.smrt_diameter])
        .separation(function (a, b) {
          return (a.parent == b.parent ? 1 : 1.5) / a.depth;
        });
      this.smrt_filteredPartition = d3.layout.partition()
        .value(function (d) { return d.value; })
        .children(function (d) {
          if (isNaN(d.value)) {
            var filteredChildren = [];
            d3.entries(d.value).forEach(function (d2) {
              if (d2.node_type != "ISSUER") filteredChildren.push(d);
            });
            return filteredChildren;
          } else {
            return null;
          }
        });
      this.smrt_radialProjection = d3.svg.diagonal.radial()
        .projection(function (d) {
          return [d.y, d.x / 180 * Math.PI];
        });
      this.smrt_svg = d3.select('#display_radial_tidy_tree').append('svg')
        .attr('preserveAspectRatio', 'xMinYMin meet')
        .attr('viewBox', '0 0 ' + this.smrt_width + ' ' + this.smrt_height)
        .append('g')
        .attr('transform', 'translate(' + this.smrt_diameter / 2 + ',' + this.smrt_diameter / 2 + ') rotate(0)');
      this.smrt_color = d3.scale.ordinal(['#3f2c70', '#fcec04']);
      this.smrt_legend = d3.select('body svg').append('g').attr('class', 'legend');
      this.smrt_angle = 0;
      this.smrt_buttons = d3.select('body svg').append('g').attr('class', 'button');
      this.update(this.smrt_root);
      d3.select(self.frameElement).style("height", "800px");
    },
    methods: {
      async getAccountGenealogy(stellar_account, network_name) {
          try {
              // Get the CSRF token from the cookie
              const csrf_token = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");

              const headers = {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrf_token
              };
              const genealogy_response = await fetch('/account-genealogy/network/' + network_name + '/stellar_address/' + stellar_account + '/', { method: 'GET', headers });

              if (!genealogy_response.ok) {
                  // Get the error message from the response
                  const error = await genealogy_response.json();
                  Sentry.captureException(error);
              }

              // parse the JSON
              const responseJson = JSON.parse(await genealogy_response.json());

              // assign to vue variables
              this.account_genealogy_items = responseJson.account_genealogy_items;
              this.tree_genealogy_items = responseJson.tree_genealogy_items;

          } catch (e) {
              // Handle error
              console.error(e);
              alert(e.message);
              Sentry.captureException(e);
          }
      },
      truncateStellarAccount(stellar_account) {
        if (stellar_account && stellar_account.length > 17) {
          // return last 6 characters of stellar address
          truncated_string = stellar_account.slice(0, 6) + '...' + stellar_account.slice(-6);
          return truncated_string;
        } else {
          return stellar_account;
        }
      },
      viewExternalLinkStellarExpert(stellar_account, network_name) {
          base_url = "https://stellar.expert/explorer/";
          url_path = base_url.concat(network_name, '/account/', stellar_account);
          return url_path;
      },
      viewTooltipString(string_name) {
        return string_name;
      },
      viewExternalLinkTOML(home_domain) {
        base_url = "https://";
        url_path = base_url.concat(home_domain, '/.well-known/stellar.toml');
        return url_path;
      },
      viewExternalLinkTOMLChecker(home_domain) {
        base_url = "https://stellar.sui.li/";
        url_path = base_url.concat(home_domain);
        return url_path;
      },
      async getApiStellarExpertTags(row_index, stellar_account, network_name) {
        const base_url = "https://api.stellar.expert/explorer/";
        const url_path = base_url.concat(network_name, '/directory/', stellar_account);
        const response = await fetch(url_path);
        this.apiStellarExpertTagsResponses[row_index] = await response.json();
        return this.apiStellarExpertTagsResponses[row_index];
      },
      formatHashtag(tag) {
        hashtag = '#';
        return hashtag.concat(tag);
      },
      update(source) {
        var nodes = this.smrt_tree.nodes(this.smrt_root),
          links = this.smrt_tree.links(nodes);
        nodes.forEach(function (d) { d.y = d.depth * 80; });
        var node = this.smrt_svg.selectAll("g.node")
          .data(nodes, function (d) { return d.id || (d.id = ++this.smrt_counter); });
        var nodeEnter = node.enter()
          .append("g")
          .attr("class", "node")
          .attr('name', d => {
            if (d.deleted == true) { return "DELETED" }
            else
              return d.node_type
          })
          .on("click", this.click)
          .on("mouseenter", this.mouseEnter)
          .on("mouseleave", this.mouseLeave);
        this.smrt_tooltip.on('mouseenter', this.tooltipMouseEnter)
          .on('mouseleave', this.tooltipMouseLeave);
        nodeEnter.append("circle")
          .attr("r", 1e-7)
          .on("mouseenter", this.circleMouseEnter);
        nodeEnter.append("text")
          .attr("x", function (d) { return d.x < Math.PI === !d.children ? 6 : 6; })
          .attr("dy", "0.31em")
          .attr("text-anchor", function (d) { return d.x < 180 ? "start" : "end"; })
          .text(function (d) { return d.name; })
          .style("fill-opacity", 1e-6);
        var nodeUpdate = node.transition()
          .duration(this.smrt_duration)
          .attr("transform", function (d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; });
        nodeUpdate.select("circle")
          .attr("r", this.smrt_diameter / 300)
          .style("fill", function (d) { return d._children ? "#fff" : "#3f2c70"; })
          .style("stroke", function (d) {
            if (d.node_type == 'ASSET') { return '#fcec04' }
            else {
              if (d.deleted == true) { return '#cc3463' }
            }
          });
        nodeUpdate.select("text")
          .style("fill-opacity", 1)
          .attr("transform", function (d) { return d.x < 180 ? "translate(0)" : "rotate(180)translate(-" + (12) + ")"; });
        var nodeExit = node.exit().transition()
          .duration(this.smrt_duration)
          .remove();
        nodeExit.select("circle")
          .attr("r", 1e-6);
        nodeExit.select("text")
          .style("fill-opacity", 1e-6);
        var link = this.smrt_svg.selectAll("path.link")
          .data(links, function (d) { return d.target.id; });
        link.enter().insert("path", "g")
          .attr("class", "link")
          .attr("id", function (d) { return ("link" + d.source.id + "-" + d.target.id) })
          .attr("name", function (d) {
            if (d.target.deleted == true) { return "DELETED" }
            else
              return (d.target.node_type)
          })
          .attr("d", function (d) {
            var o = { x: source.x0, y: source.y0 };
            return this.smrt_radialProjection({ source: o, target: o });
          });
        link.transition()
          .duration(this.smrt_duration)
          .attr("d", this.smrt_radialProjection);
        link.exit().transition()
          .duration(this.smrt_duration)
          .attr("d", function (d) {
            var o = { x: source.x, y: source.y };
            return this.smrt_radialProjection({ source: o, target: o });
          })
          .remove();
        nodes.forEach(function (d) {
          d.x0 = d.x;
          d.y0 = d.y;
        });
      },
      click(d) {
        if (d.children) {
          d._children = d.children;
          d.children = null;
        } else {
          d.children = d._children;
          d._children = null;
        }
        this.update(d);
      },
      mouseEnter(d) {
        var lineage = [];
        var type = [];
        d3.selectAll("circle").style("fill", "#3f2c70");
        d3.selectAll("path").style("stroke", "#3f2c70");
        while (d.parent) {
          d3.selectAll("#node" + d.id).style("fill", "red")
          if (d.parent != "null") {
            lineage.push(d.name)
            if (d.node_type == 'ASSET') { type.push('#fcec04') }
            else {
              if (d.deleted == true) { type.push('#cc3463') }
              else
                type.push("#00FF9C")
            }
            d3.selectAll("#link" + d.parent.id + "-" + d.id).style("stroke", "red")
          }
          d = d.parent;
        }
        for (i = lineage.length - 1; i >= 0; i--) {
          this.smrt_navbars.append('a').attr('class', 'breadcrumbs__item')
            .style('background', type[i])
            .append('text')
            .style('fill', 'black')
            .text(lineage[i])
            .append('div').attr('class', 'after').style('background', type[i])
        }
      },
      mouseLeave() {
        this.smrt_tooltip.style("opacity", 0);
        d3.selectAll("circle").style("fill", "#3f2c70");
        d3.selectAll("path").style("stroke", "#3f2c70");
        d3.selectAll('.breadcrumbs__item').remove();
      },
      tooltipMouseEnter() {
        d3.select(this).style("opacity", 1);
      },
      tooltipMouseLeave() {
        d3.select(this).style("opacity", 0)
          .html("")
          .style("left", (0) + "px")
          .style("top", (0) + "px");
      },
      circleMouseEnter(d) {
        if (d.node_type == 'ASSET') {
          this.smrt_tooltip.style("opacity", 0.71).style("background-color", '#fcec04')
          this.smrt_tooltip
            .html("<b>Name:</b> " + d.name + "<br><b>Issuer Id:</b> " + d.issuer_id
              + "<br><b>Asset type:</b> " + d.asset_type
              + "<br><b>Asset Code:</b> " + d.asset_code
              + "<br><b>Asset Issuer:</b> " + d.asset_issuer
              + "<br><b>Balance:</b> " + d.balance
              + "<br><b>Limit:</b> " + d.limit
              + "<br><b>Is Authorized:</b> " + d.is_authorized
              + "<br><b>Is Authorized To Maintain Liabilities:</b> " + d.is_authorized_to_maintain_liabilities
              + "<br><b>Is Clawback Enabled:</b> " + d.is_clawback_enabled
              + "<br><b>Stellar Expert:</b> <a href=" + d.stellar_expert + ">Link</a>"
              + "<br><b>Number of Accounts:</b> " + d.num_accounts
              + "<br><b>Number of Claimable Balances:</b> " + d.num_claimable_balances
              + "<br><b>Num of Liquidity Pools:</b> " + d.num_liquidity_pools
              + "<br><b>Amount:</b> " + d.amount
            )
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY) + "px")
        }
        else {
          this.smrt_tooltip.style("opacity", 0.71).style("background-color", '#00FF9C')
          if (d.deleted == true) {
            this.smrt_tooltip.style("opacity", 0.71).style("background-color", '#cc3463')
          }
          this.smrt_tooltip
            .html("<b>Stellar Account:</b> " + d.stellar_account
              + "<br><b>Created:</b> " + d.created
              + "<br><b>Creator Account:</b> " + d.home_domain
              + "<br><b>Home Domain:</b> " + d.home_domain
              + "<br><b>XLM Balance:</b> " + d.xlm_balance)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY) + "px")
        }
        if (d.x < 90 && d.x > 0) {
          this.smrt_tooltip
            .style("left", (d3.event.pageX - this.smrt_tooltip.node().offsetWidth) + "px")
            .style("top", (d3.event.pageY) + "px")
        }
        else if (d.x < 180 && d.x > 90) {
          this.smrt_tooltip
            .style("left", (d3.event.pageX - this.smrt_tooltip.node().offsetWidth) + "px")
            .style("top", (d3.event.pageY - this.smrt_tooltip.node().offsetHeight) + "px")
        }
        else if (d.x < 270 && d.x > 180) {
          this.smrt_tooltip
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - this.smrt_tooltip.node().offsetHeight) + "px")
        }
      },
      collapse(d) {
        if (d.children) {
          d._children = d.children;
          d._children.forEach(this.collapse);
          d.children = null;
        }
      }
    },
    computed: {
      visibleGeneologyFields() {
        return this.account_genealogy_fields.filter(field => field.visible)
      }
    },
    watch: {
      account_genealogy_items: {
        deep: true,
        handler(newVal, oldVal) {
          if (newVal !== oldVal) {
            newVal.forEach((item) => {
              this.getApiStellarExpertTags(item.index, item.stellar_account, item.network_name);
            });
          }
        },
      },
    }
  }

  