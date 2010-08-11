/* I realize that I ought to be using a Javascript compressor such as Google's
 * Closure Compiler (http://closure-compiler.appspot.com). However, my intent,
 * Gentle Reader, is to use this web site to convince you that I'm an adept
 * programmer, and this ought to be more easily accomplished if the intricacies
 * of my labours are visible with only a "View Source" on your part.
 * Altogether, I deem this ability worth the several kilobyte cost. Of course,
 * this comment alone has consumed another half-kilobyte, which makes me feel
 * like a darned fool. */

$(document).ready(function() {
  var misc = new Miscellany();

  new AboutTidbitSwitcher(misc);
  new ProjectSwitcher(misc);
  new ProjectImageSwitcher();
  new ContactForm();

  // If '#navigation a' selector is used, then elements shift down two pixels
  // when their positions are locked. This may be due to the anchors being
  // converted from inline elements to block-level elements when they are
  // absolutely positioned. Regardless, changing the selector to '#navigation
  // li' fixes this.
  new TextInflater('#navigation li', 1.15);

  misc.dispatch_router();
});



/*==========
  Miscellany
  ==========*/
function Miscellany() {
  this._configure_miscellany();
}

Miscellany.prototype._configure_miscellany = function() {
  this._clone_content('.about_tidbit', 3);
  this._clone_content('.project_detail', 7);
  $('.project_detail.active').not(':first').removeClass('active');
  this._clone_content('#slartibartfast_trigger', 5);
  this._configure_guide_toggler();

  var router = this._configure_router();
  this._configure_smooth_scroller(router);
}

// To scroll to the appropriate project, this function must be called only
// after the appropriate horizontal scroller is set up, which occurs when
// ProjectSwitcher is instantiated.
Miscellany.prototype.dispatch_router = function() {
  this._router.dispatch();
}

Miscellany.prototype.create_horizontal_scroller = function(trigger_selector, panel_selector,
panels_container_selector, on_trigger) {
  var triggers         = $(trigger_selector);
  var panels           = $(panel_selector);
  var panels_container = $(panels_container_selector);

  if(triggers.length != panels.length)
    throw 'Number of triggers different from number of panels';

  triggers.click(function(event_data, extra_params) {
    // By returning non-true value from on_trigger(), clients can halt the
    // panel-switching animation.
    if(!on_trigger(event_data, extra_params, triggers, $(this)))
      return;

    var selected_panel = panels.eq(triggers.index(this));
    panels.removeClass('active');
    selected_panel.addClass('active');
    var offset = -(selected_panel.position().left - panels.eq(0).position().left);
    panels_container.animate({ marginLeft: offset }, { duration: 900 });
  });
}

Miscellany.prototype._configure_router = function() {
  this._router = new UrlHashRouter();

  var self = this;
  this._router.register_route(new RegExp('^/work/(.+)$'), function(match) {
    self._scroll_to('#work');
    var project = match[1];
    var trigger = $('#' + project + '_trigger');
    trigger.click();
  });
  this._router.register_route(new RegExp('^/([^/]+)$'), function(match) {
    self._scroll_to('#' + match[1]);
  });
}

Miscellany.prototype._clone_content = function(to_clone, times) {
  to_clone = $(to_clone);
  for(var i = 0; i < times; i++)
    to_clone.clone().appendTo(to_clone.parent());
}

Miscellany.prototype._configure_smooth_scroller = function(router) {
  var self = this;
  $('a[href*=#]').click(function () {
    // Only intercept links leading to locations on current page.
    if(this.host != window.location.host ||
      this.pathname != window.location.pathname)
      return true;

    var hash = this.hash;
    var was_element_found = self._scroll_to('#' + hash.substring(2)); // Strip initial '#/'.
    if(!was_element_found)
      return true; // Element doesn't exist, so continue with browser's normal link processing.

    window.location.hash = hash.substring(1); // Strip initial '#'.
    return false;
  });
}

Miscellany.prototype._scroll_to = function(elem) {
  this._fixed_header_height = $('#header').outerHeight();

  var target = $(elem);
  if(target.length == 0)
    return false;

  this._pad_bottom(target);

  // Chrome requires scrollTop be set on 'body'; Firefox requires it be set on 'html'.
  $('html, body').animate({
    scrollTop: target.offset().top - this._fixed_header_height
  }, 1000);
  return true;
}

// Dynamically pad bottom of document if necessary, so that when we scroll to
// element, that element will always appear at top of viewport, even if it is
// near the document's bottom.
Miscellany.prototype._pad_bottom = function(elem) {
  // Vertical space from top of elem to bottom of document.
  var vertical_space = $(document).height() - $(elem).offset().top;
  // Height of viewport for content, which excludes our fixed-position header.
  var viewport_height = $(window).height() - this._fixed_header_height;
  var diff = vertical_space - viewport_height;

  // If viewport is taller than space from top of element to bottom of
  // document, pad bottom of last content section appropriately.
  if(diff < 0) {
    // Last section is footer, so get section before that.
    var last_content_section = $('.section.last').prev('.section');
    var new_padding = -diff + parseInt(last_content_section.css('paddingBottom'), 10);
    last_content_section.css('paddingBottom', new_padding);
  }
}

Miscellany.prototype._configure_guide_toggler = function() {
  $(document).keydown(function(event) {
      if(event.keyCode === 71) $('#guide').toggle();
  });
}



/*===============
  ProjectSwitcher
  ===============*/
function ProjectSwitcher(misc) {
  misc.create_horizontal_scroller('#project_list .project', '.project_detail',
    '#projects_detail_container',
    function(event_data, extra_params, triggers, activated_trigger) {
      window.location.hash = '/work/' + activated_trigger.attr('id').replace('_trigger', '');
      return (new BorderAnimator(triggers, activated_trigger)).animate();
    });
}



/*===================
  AboutTidbitSwitcher
  ===================*/
function AboutTidbitSwitcher(misc) {
  this._container = $('#about_tidbits');
  this._triggers = this._container.find('.trigger');
  this._configure_scroller(misc);
  this._configure_auto_switcher();
}

AboutTidbitSwitcher.prototype._configure_scroller = function(misc) {
  var self = this;
  misc.create_horizontal_scroller(this._triggers, '.about_tidbit',
    '#about_tidbits_container',
    function(event_data, extra_params, triggers, activated_trigger) {
      // Click was generated by a human, not our automated switcher.
      if(!(extra_params && extra_params.auto_generated)) {
        self._halt_auto_switcher();
      }

      triggers.removeClass('active');
      activated_trigger.addClass('active');
      return true;
    });
}

AboutTidbitSwitcher.prototype._configure_auto_switcher = function() {
  var self = this;

  this._auto_switcher_timer = setInterval(function() {
    var next_trigger_index = 1 +
      self._triggers.index(self._triggers.filter('.active'));
    if(next_trigger_index === self._triggers.length)
      next_trigger_index = 0;
    self._triggers.eq(next_trigger_index).trigger('click',
      { auto_generated: true });
  }, 10000);
}

AboutTidbitSwitcher.prototype._halt_auto_switcher = function() {
  clearInterval(this._auto_switcher_timer);
}



/*==============
  BorderAnimator
  ==============*/
function BorderAnimator(triggers, activated_trigger) {
  this._old_selected = triggers.filter('.active');
  this._new_selected = activated_trigger;
  this._animation_duration = 450;
}

BorderAnimator.prototype.animate = function() {
  // If an animation is currently in progress, there will be no "active"
  // element (as the class has been removed), and so we must halt before going
  // further.
  if(this._old_selected.length === 0)
    return false;

  this._create_border();

  // Must use "self" rather than relying on "this", as the on_complete
  // callbacks of _enlarge() and _reduce() are called by jQuery, which will set
  // "this" (using apply()) to the element on which the animation is being
  // applied -- that is, this._animated_border. Were it not to do so, given
  // that I create the on_complete callbacks as an anonymous functions, "this"
  // would refer to the "global" object ("window"), as it does for any
  // function.
  var self = this;
  self._enlarge(function() {
    self._reduce(function() {
      self._new_selected.addClass('active');
      self._animated_border.remove();
    });
  });
  return true;
}

BorderAnimator.prototype._create_border = function() {
  this._animated_border = $('<div id="animated_border"/>');
  this._animated_border.css({
    border:       '1px solid #cbcbcb',
    borderLeft:   '1px solid #f2f2f2',
    position:     'absolute',
    left:         '0px',
    // innerHeight() and innerWidth() values include padding, which is desired.
    height:       this._old_selected.innerHeight(),
    width:        this._old_selected.innerWidth(),
    cursor:       'pointer'
  });

  this._animation_direction = this._new_selected.position().top >
    this._old_selected.position().top ? 'down' : 'up';

  if(this._animation_direction === 'down') {
    var pos = { top: this._calc_top_border_y(this._old_selected) + 'px' };
  } else if(this._animation_direction === 'up') {
    var pos = { bottom: this._old_selected.offsetParent().height() -
      this._calc_bottom_border_y(this._old_selected) + 'px' };
  }
  this._animated_border.css(pos).appendTo('#project_list');
}

BorderAnimator.prototype._enlarge = function(on_complete) {
  this._old_selected.removeClass('active');

  if(this._animation_direction === 'down') {
    var height = this._calc_bottom_border_y(this._new_selected) -
      this._calc_top_border_y(this._old_selected);
  } else if(this._animation_direction === 'up') { 
    var height = this._calc_bottom_border_y(this._old_selected) -
      this._calc_top_border_y(this._new_selected);
  }

  this._animated_border.animate({ height: height }, {
    duration: this._animation_duration,
    complete: on_complete
  });
};

BorderAnimator.prototype._reduce =  function(on_complete) {
  if(this._animation_direction === 'down') {
    var bottom = this._new_selected.position().top +
      this._new_selected.outerHeight(true);
    this._animated_border.css({
      top:    'auto',
      bottom: this._animated_border.offsetParent().height() - bottom
    });
  } else if(this._animation_direction === 'up') {
    this._animated_border.css({
      bottom: 'auto',
      top:    this._new_selected.position().top
    });
  }

  // BUG: this._new_selected.innerHeight()'s value will be two pixels greater
  // than it ought to be, for when the "active" class is applied to the
  // element, its vertical padding shrinks by a combined two pixels to
  // compensate for the two vertical pixels occupied by its border. We could
  // try to compensate for this, but the effect of the bug is rather small --
  // effectively, the height of the element is reduced via the animate() call
  // to a value two pixels greater than it should be, followed by the height
  // immediately "jumping" two pixels shorter when the "active" class is
  // applied in the on_complete callback. Given that this two-pixel jump is
  // hardly noticeable to the eye, it's not worth jumping through multiple
  // hoops to correct it. If the border (and thus the compensatory padding)
  // occupied more than two vertical pixels, we might have to consider such a
  // fix, however.
  this._animated_border.animate({
    height: this._new_selected.innerHeight() + 'px'
  }, { duration: this._animation_duration, complete: on_complete });
}

BorderAnimator.prototype._calc_top_border_y = function(elem) {
  return elem.position().top + parseInt(elem.css('marginTop'), 10);
}

BorderAnimator.prototype._calc_bottom_border_y = function(elem) {
  return elem.position().top + elem.outerHeight(true) -
    parseInt(elem.css('marginBottom'), 10);
}






/*============
  TextInflater
  ============*/
function TextInflater(elements, factor) {
  this._elements = $(elements);

  var self = this;
  this._elements.hover(function() {
    // Lock positions only on first hover, not during initialization. If done
    // during initiazliation, occasionally (especially when loading page from
    // remote server, and especially when using Chrome) this code will run
    // *before* the elements being inflated have been laid out at their proper
    // positions, resulting in the elements being "locked" into a position
    // where they ought not to be. Running the code only on first hover gives
    // the browser time to properly lay out the elements before this code runs.
    self._lock_positions();

    var element = $(this);
    // We must store the base_font_size, as if we simply fetch the font size on
    // each hover event, then bad things happen when a resizing animation is
    // triggered while a previous one is still in progress (i.e., the user
    // hovers over the element, moves his mouse out, then quickly hovers over
    // it again). In such a case, the element's font size will be in flux
    // because the resizing animation will still be adjusting it step-by-step,
    // resulting in the font size ending up at a value different from before
    // any animations were triggered.
    //
    // Note that fontSize may not be an integer, and so must be stored as a
    // float.
    if(element.data('base_font_size') === undefined) {
      element.data('base_font_size', parseFloat(element.css('fontSize')));
    }
    self._adjust_size(element, factor);
  }, function() {
    self._adjust_size($(this), 1);
  });
}

// Postion text with absolute positioning to remove it from the normal flow.
// This way, font size adjustments won't cause adjacent elements to be
// repositioned.
TextInflater.prototype._lock_positions = function() {
  if(this._positions_locked)
    return;
  this._positions_locked = true;

  // Must store positions first -- if we absolutely positioned each element
  // without first storing its initial position, elements after the first would
  // be repositioned as the elements before them are removed from the normal
  // flow.
  var positions = [];
  this._elements.each(function() {
    var element = $(this);
    positions.push([element, element.position()]);
  });

  $.each(positions, function(i, position) {
    position[0].css({
      position: 'absolute',
      left:     position[1].left,
      top:      position[1].top
    });
  });
}

TextInflater.prototype._adjust_size = function(element, factor) {
  element.animate({
    fontSize: factor*element.data('base_font_size')
  }, { duration: 200, queue: false });
}



/*=============
  UrlHashRouter
  =============*/
function UrlHashRouter() {
  this._routes = [];

}

UrlHashRouter.prototype.dispatch = function() {
  var hash = window.location.hash.substring(1); // Strip leading '#'.

  for(var i = 0; i < this._routes.length; i++) {
    var pattern = this._routes[i][0];
    var callback = this._routes[i][1];
    var result = pattern.exec(hash);
    if(result)
      callback(result);
  }
}

UrlHashRouter.prototype.register_route = function(path, callback) {
  this._routes.push([path, callback]);
}



/*===========
  ContactForm
  ===========*/
function ContactForm() {
  $('#contact_form form').submit(function() {
    var visible_elements = $(this).find('.label_and_error, input, textarea').toArray();
    // Sort randomly.
    visible_elements.sort(function(a, b) {
      return Math.random() - 0.5;
    });

    var disappear = function(on_complete) {
      if(visible_elements.length === 0) return on_complete();

      var element = visible_elements.pop();
      $(element).css('visibility', 'hidden');

      setTimeout(function() { disappear(on_complete); }, 100);
    };

    var self = $(this);
    disappear(function() {
      var container = self.parent();
      // Explicitly set height of container so that when its contents are
      // changed, elements below it don't reflow.
      container.css('height', container.height());
      self.empty();
      $('<p>Thanks!</p>').css('display', 'none').appendTo(self).slideDown();
    });
    return false;
  });
}



/*====================
  ProjectImageSwitcher
  ====================*/
function ProjectImageSwitcher() {
  this._configure_controls_display();
  this._configure_controls_action();
}

ProjectImageSwitcher.prototype._configure_controls_display = function() {
  var active_project_images = $('.project_detail.active .project_images');
  var animation_duration = 250;

  // Use 'live' events since active project changes over time.
  active_project_images.find('img').live('mouseenter', function() {
    $(this).parents('.project_images').find('.project_image_controls').slideDown(animation_duration);
  });

  active_project_images.live('mouseleave', function() {
    $(this).find('.project_image_controls').slideUp(animation_duration);
  });
}

ProjectImageSwitcher.prototype._configure_controls_action = function() {
  $('.project_image_controls .prev, .project_image_controls .next').click(function() {
    var container        = $(this).parents('.project_images');
    var image_container  = container.find('.image_container');

    var prev_active = image_container.find('.active');
    prev_active.removeClass('active')

    if($(this).hasClass('next')) {
      var new_active = prev_active.next();
      var default_pos = 'first';
    } else {
      var new_active = prev_active.prev();
      var default_pos = 'last';
    }

    if(new_active.length === 0)
      new_active = image_container.find('img:' + default_pos);

    new_active.addClass('active');
    image_container.animate({ marginLeft: -new_active.position().left }, { duration: 300 });
  });
}