/* Module for working with multiple field inputs. This will create
 * a new field when the user clicks the 'add field' button.
 *
 */
this.ckan.module('composite-repeating', function (jQuery, _) {
  return {
    options: {
      /* The selector used for each custom field wrapper */
      fieldSelector: '.composite-control-repeating'
    },

    /* Initializes the module and attaches custom event listeners. This
     * is called internally by ckan.module.initialize().
     *
     * Returns nothing.
     */
    initialize: function () {

      if (!jQuery('html').hasClass('ie7')) {
        jQuery.proxyAll(this, /_on/);

        // Create 'minus field' checkbox and add to first input of every container.
        function getMinusButton(index){
            var checkbox_minus = $('<label class="checkbox btn btn-danger fa fa-minus composite-btn " ><input type="checkbox" /></label>');
                        
            checkbox_minus.attr("id", "label-remove-field-" + index);
            checkbox_minus.attr("name", "label-remove-field-" + index);
            checkbox_minus.find(':checkbox').attr("id", "remove-field-" + index);
            checkbox_minus.find(':checkbox').attr("name", "remove-field-" + index);
            return checkbox_minus;
        }

        var onChangeFn = this._onChange;
        var fieldContainers = this.el.find(this.options.fieldSelector);
        $(fieldContainers).each(function(index) {$(this).find('.controls:first').append(getMinusButton(index+1))});
        $(fieldContainers).find('.controls:first').find(".fa-minus").each(function() { $(this).on('change', ':checkbox', onChangeFn); $(this).children(':checkbox').hide();});

        // Create 'plus field' checkbox and add to first input container.
        var firstFieldContainer = this.el.find(this.options.fieldSelector + ':first .controls:first');

        var checkbox = $('<label class="checkbox btn btn-success fa fa-plus composite-btn" style="margin-top:3px;" ><input type="checkbox" id="add-field" style="padding:5px;"/></label>');
        checkbox.on('change', ':checkbox', this._onChange);
	    checkbox.children(':checkbox').hide();
        $(firstFieldContainer).append(checkbox);
      }
    },

    /* Create a new field and appends it to the list. This currently works by
     * cloning and erasing an existing input rather than using a template.
     * In future using a template might be more appropriate.
     *
     * element - Another custom field element to wrap.
     *
     * Returns nothing.
     */
    newField: function (element) {
      newEl = this.cloneField(element);
      this.el.append(newEl);
    },

    /* Clone the provided element, wipe its content and increment its
     * `for`, `id` and `name` fields (if possible).
     *
     * current - A custom field to clone.
     *
     * Returns a newly created custom field element.
     */
    cloneField: function (current) {
      return this.resetField(jQuery(current).clone(true,true));
    },

    /* Wipe the contents of the field provided and increment its `name`, `id`
     * and `for` attributes. Also remove 'add' checkbox if necessary. Also
     * remove info - button.
     *
     * field - A custom field to wipe.
     *
     * Returns the wiped element.
     */
    resetField: function (field) {
      function increment(index, string) {
        return (string || '').replace(/\d+/, function (int) { return 1 + parseInt(int, 10); });
      }

      var input = field.find(':input');
      input.attr('id', increment).attr('name', increment);
      // remove value except for checkboxes
      input.each(function(){ if (! ($(this).hasClass("composite-multiple-checkbox"))) {$(this).val('')}});

      // unselect checkboxes
      input.filter('.composite-multiple-checkbox').attr("checked", false);
      
      var label = field.find('label');
      label.each(function(){ if (! ($(this).hasClass("fa-minus"))) {$(this).attr('for', increment)}});
      label.each(function(){ if ($(this).hasClass("control-label")) {$(this).text(increment)}});

      field.find('.fa-plus').remove();
      field.find('button.outsidebutton').remove();

      return field;
    },
    deleteField: function(target){
        var index = parseInt(target.id.split("-").pop());
        var field = $(target).parents(".composite-control-repeating").first();
        if (index>1) {
            field.remove();
        }
        else {
            field.find(':input').val('');
        }
    },
    /* Event handler called when the add checkbox is changed */
    _onChange: function (event) {
      if (event.currentTarget.id === "add-field"){
          var lastFieldContainer = this.el.find(this.options.fieldSelector + ':last');
          this.newField(lastFieldContainer);
      }
      else{
          this.deleteField(event.currentTarget);
      }
    }
  };
});

