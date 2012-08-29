// Models
window.MediaItem = Backbone.Model.extend({
    idAttribute: 'item_id',
});

window.MediaItemCollection = Backbone.Collection.extend({
    model:MediaItem,
    url: '/api/1.0/all_music',
    parse: function(resp, xhr) {
        //this.header = resp.header;
        //this.stats = resp.stats;
        return resp.all_music;
    },
});


// Views
window.MediaItemListView = Backbone.View.extend({

    tagName:'ul',

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        _.each(this.model.models, function (item) {
            $(this.el).append(new MediaItemListView({model:item}).render().el);
        }, this);
        return this;
    }

});

window.MediaItemListItemView = Backbone.View.extend({

    tagName:"li",

    template:_.template($('#tpl-item-list-item').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});

window.MediaItemView = Backbone.View.extend({

    template:_.template($('#tpl-item-details').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});


// Router
var AppRouter = Backbone.Router.extend({

    routes:{
        "":"list",
        "items/:id":"MediaItemDetails"
    },

    list:function () {
        this.MediaItemList = new MediaItemCollection();
        this.MediaItemListView = new MediaItemListView({model:this.MediaItemList});
        this.MediaItemList.fetch();
        $('#sidebar').html(this.MediaItemListView.render().el);
    },

    MediaItemDetails:function (id) {
        this.MediaItem = this.MediaItemList.get(id);
        this.MediaItemView = new MediaItemView({model:this.MediaItem});
        $('#content').html(this.MediaItemView.render().el);
    }
});

var app = new AppRouter();
Backbone.history.start();