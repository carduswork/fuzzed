define(['dfd/config', 'node', 'jquery', 'jsplumb'], function(Config, AbstractNode) {
    /**
     * Package: DFD
     */

    /**
     * Class: DFDNode
     *      DFD node subclass. Mainly adapts the connector/edge style to be free-form instead of tree-like.
     *
     * Extends: <Base::Node>
     */
    return AbstractNode.extend({
        getConfig: function() {
            return Config;
        },

        _connectorAnchors: function() {
            return {
                'in':  [0.5, 0, 0, 0],
                'out': [0.5, 0, 0, 0]
            }
        },

        _connectorOffset: function() {
            var topOffset = this._nodeImageContainer.outerWidth(true) / 2;

            return {
                'in': {
                    'x': 0,
                    'y': topOffset
                },
                'out': {
                    'x': 0,
                    'y': topOffset
                }
            }
        },

        _setupConnectionHandle: function() {
            if (this.numberOfOutgoingConnection == 0) return this;

            var position = this._nodeImageContainer.position();
            var stroke   = this.config.JSPlumb.STROKE_WIDTH;

            this._connectionHandle = jQuery('<i class="fa fa-plus"></i>')
                .addClass(this.config.Classes.NODE_HALO_CONNECT)
                .css({
                    'top':  position.top  + this._nodeImage.outerHeight(true) / 2 + stroke * 1.5,
                    'left': position.left + this._nodeImage.outerWidth(true)  / 2
                })
                .appendTo(this.container);

            return this;
        },
        
        _calc_anchor: function(anchorCount, offset){
            var _circle = function() {
                var radius  = 0.5;
                var step    = Math.PI * 2 / anchorCount;
                var current = offset * step;
                var all     = [];

                for (var i = 0; i < anchorCount; ++i) {
                    var x = radius + (radius * Math.cos(current));
                    var y = radius + (radius * Math.sin(current));

                    all.push([x, y, 0, 0]);
                    current += step;
                }
                return all;
            };

            return _circle();
        },

        _sourceAnchors: function(){
            return this._calc_anchor(8, 0.25);
        },

        _targetAnchors: function(){
            return this._calc_anchor(8, -0.25);
        },

        _setupIncomingEndpoint: function() {
            if (this.numberOfIncomingConnections === 0) return this;

            jsPlumb.makeTarget(this.container, {
                // position of the anchor
                anchor:         this._targetAnchors(),
                maxConnections: this.numberOfIncomingConnections,
                dropOptions: {
                    // Define which node can connect to the target...
                    accept: function(draggable) {
                        var elid = draggable.attr('elid');
                        // ...DOM elements without elid (generated by jsPlumb) are disallowed...
                        if (typeof elid === 'undefined') return false;

                        // ...as well as nodes without a node object representing it.
                        var sourceNode = jQuery('.' + this.config.Classes.NODE + ':has(#' + elid + ')').data('node');
                        if (typeof sourceNode === 'undefined') return false;

                        // Ask the source node if it can connect to us.
                        return sourceNode.allowsConnectionsTo(this);
                    }.bind(this),
                    activeClass: this.config.Classes.NODE_DROP_ACTIVE
                }
            });

            return this;
        },

        _setupOutgoingEndpoint: function() {
            if (this.numberOfOutgoingConnections == 0) return this;

            // small flag for the drag callback, explanation below
            var highlight     = true;
            var inactiveNodes = '.' + this.config.Classes.NODE + ':not(.'+ this.config.Classes.NODE_DROP_ACTIVE + ')';

            jsPlumb.makeSource(this._connectionHandle, {
                parent:         this.container,
                anchor:         this._sourceAnchors(),
                maxConnections: this.numberOfOutgoingConnections,
                connectorStyle: this.connector,//[this.config.JSPlumb.CONNECTOR_STYLE, { curviness: 30, stub: 5}],
                dragOptions: {
                    cursor: this.config.Dragging.CURSOR_EDGE,
                    // XXX: have to use drag callback here instead of start
                    // The activeClass assigned in <Node::_setupIncomingEndpoint> is unfortunately assigned only AFTER
                    // the execution of the start callback by jsPlumb.
                    drag: function() {
                        // using the highlight flag here to simulate only-once-behaviour (no re-computation of node set)
                        if (!highlight) return;
                        // disable all nodes that can not be targeted
                        jQuery(inactiveNodes).each(function(index, node){
                            jQuery(node).data(this.config.Keys.NODE).disable();
                        }.bind(this));
                        highlight = false;
                    }.bind(this),
                    stop: function() {
                        // re-enable disabled nodes
                        jQuery(inactiveNodes).each(function(index, node){
                            jQuery(node).data(this.config.Keys.NODE).enable();
                        }.bind(this));
                        // release the flag, to allow fading out nodes again
                        highlight = true;
                    }.bind(this)
                }
            });

            return this;
        }
    });
});
