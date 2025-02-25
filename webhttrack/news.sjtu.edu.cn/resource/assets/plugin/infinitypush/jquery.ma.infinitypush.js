Copyright (c) 2014 Marc Andrew http://marcandrew.net/off-canvas-infinity-push

MIT License (http://www.opensource.org/licenses/mit-license.html)
*/

;(function($){

	$.fn.infinitypush = function(options){

		/**
		 * Default options
		 */

		var defaults = {
			offcanvas			: true,
			offcanvasspeed		: 400,
			offcanvasleft		: true,
			openingspeed		: 400,
			closingspeed		: 400,
			spacing				: 90,
			pushdirectionleft	: true,
			autoScroll			: true,
			scrollSpeed			: 300,
			destroy				: false
		};

		var infinityPushWrapper = this;

		var opts = $.extend( {}, defaults, options );

		/**
		 * Start Navigation functions
		 */

		return this.each(function() {

			var oldposition			= $(this).data('oldposition') || $('body'),
				navWrapper			= 'ma-infinitypush-wrapper',
				navWrapperDiv		= '<div class="' + navWrapper + '"></div>',
				navButtonActive		= 'ma-infinitypush-active-button',
				navButton			= 'ma-infinitypush-button',
				navButtonDiv		= '<div class="' + navButton + '"></div>',
				infinityPush		= 'ma-infinitypush',
				infinityPushOpen	= 'ma-infinitypush-open';
			
			function destroy(){
				$('.' + navButton).unbind();
				$('.' + infinityPush).unbind();
				$('body').removeClass(infinityPushOpen);
				$('.' + navWrapper).next().removeAttr('style');
				$('.' + navWrapper).find('.ma-infinitypush-inactive').removeClass('ma-infinitypush-inactive');
				$('.' + navWrapper).find('.ma-infinitypush-active-item').removeClass('ma-infinitypush-active-item');
				$('.' + navWrapper).find('.ma-infinitypush-close-subnav').remove();
				$('.' + navWrapper).find('ul').removeAttr('style');
				infinityPushWrapper.prependTo(oldposition);
				infinityPushWrapper.removeClass('ma-infinitypush ma-infinitypush-sub-open');
				$('.' + navWrapper).remove();
				$(this).removeClass(infinityPush);
				infinityPushWrapper.stop().removeAttr('style');
			}
			
			if(opts.destroy){
				if($(this).hasClass(infinityPush))
					destroy();
				return;
			}
			
				// Start navigation toggle function
				function infinityPushToggle() {

					$('.' + navButton).on('click', function(){

						if($('body').hasClass(infinityPushOpen)){
							closingAnimation();
						}
						else {
							openingAnimation();
						}

					});

				}	
			
			if(!$(this).hasClass(infinityPush)){
				
				$(this).data('oldposition', $(this).parent());
				
				// Move navigation after body
				if(!$(this).parent().is('body')) {
					$('body').prepend($(this));
				}

				// Wrapping the element & add new class name
				$(this).before(navWrapperDiv).addClass(infinityPush).appendTo('.' + navWrapper);

				var navWidth	= $('.' + navWrapper).width();

				// Add the mobile menu button
				if(opts.offcanvas == true) {
					$(this).before(navButtonDiv);

					if(opts.offcanvasleft == true) {
						$('.' + navWrapper).css({ left: '-' + navWidth + 'px' });
						$('.' + navWrapper).addClass('ma-infinitypush-button-left');
					} else {
						$('.' + navWrapper).css({ right: '-' + navWidth + 'px' });
						$('.' + navWrapper).addClass('ma-infinitypush-button-right');
					}

					if(opts.pushdirectionleft == true) {
						$('.' + navWrapper).addClass('ma-infinitypush-left');
					} else {
						$('.' + navWrapper).addClass('ma-infinitypush-right');
					}

					$('.' + navWrapper).addClass(navButtonActive);
					infinityPushToggle();
				}



				// Start closing animation function
				function closingAnimation() {

					if(opts.offcanvasleft == true) {
						$('.' + navWrapper).stop().animate({
							left: '-' + navWidth + 'px'
						}, opts.offcanvasspeed);
					} else {
						$('.' + navWrapper).stop().animate({
							right: '-' + navWidth + 'px'
						}, opts.offcanvasspeed);
					}

					$('.' + infinityPush).stop().animate({
						opacity: 'hide'
					}, opts.offcanvasspeed);

					if(opts.offcanvasleft == true) {
						$('.' + navWrapper).next().stop().animate({
							left: 0
						}, opts.offcanvasspeed);
					} else {
						$('.' + navWrapper).next().stop().animate({
							right: 0
						}, opts.offcanvasspeed);
					}

					$('body').removeClass(infinityPushOpen);

				}

				// Start opening animation
				function openingAnimation() {

					$('body').addClass(infinityPushOpen);

					if(opts.offcanvasleft == true) {
						$('.' + navWrapper).stop().animate({
							left: 0
						}, opts.offcanvasspeed);
					} else {
						$('.' + navWrapper).stop().animate({
							right: 0
						}, opts.offcanvasspeed);
					}

					$('.' + infinityPush).stop().animate({
						opacity: 'show'
					}, opts.offcanvasspeed);

					if(opts.offcanvasleft == true) {
						$('.' + navWrapper).next().stop().animate({
							left: navWidth + 'px'
						}, opts.offcanvasspeed);
					} else {
						$('.' + navWrapper).next().stop().animate({
							right: navWidth + 'px'
						}, opts.offcanvasspeed);
					}

					clickOutside();

				}

				// Start closing function by clicking outside the infinity navigation
				function clickOutside() {

					$('.' + infinityPushOpen).on("mousedown touchstart", function (e) {

						if($('.' + infinityPushOpen).length) {
							if (!$('.' + navWrapper).is(e.target) // if the target of the click isn't the container...
								&& $('.' + navWrapper).has(e.target).length === 0) // ... nor a descendant of the container
							{
								closingAnimation();
							}
						}

					});

				}

				// Start infinity push function
				$('.' + infinityPush).on('click', 'a', function(){

					// General settings
					var navWidth		= $(infinityPushWrapper).width(),
						headParentUL	= $(this).parents(infinityPushWrapper).children('ul'),
						directParentUL	= $(this).closest('ul'),
						subUL			= $(this).parent().find('ul').first(),
						closeSubName	= 'ma-infinitypush-close-subnav',
						closeSubLink	= '<a href="#" class="' + closeSubName +'"></a>',
						inactiveList	= 'ma-infinitypush-inactive',
						inactiveItem	= 'ma-infinitypush-active-item',
						subOpen 		= 'ma-infinitypush-sub-open';

					if ( headParentUL.hasClass(inactiveList) && headParentUL.siblings().not(inactiveList) ) {
					// Top UL has the class name & the siblings has not the class name

						/**
						 * If statement for closing or opening the menu list
						 */

						if( directParentUL.hasClass(inactiveList) ){
						// Parent UL has the class name, close the sub menu

							// Closing animation
							if(opts.pushdirectionleft == true) {
								directParentUL.find('ul').animate({
									right: -(navWidth - opts.spacing),
									opacity: 'hide'
								}, opts.closingspeed);
							} else {
								directParentUL.find('ul').animate({
									left: -(navWidth - opts.spacing),
									opacity: 'hide'
								}, opts.closingspeed);
							}

							// Removing the class name
							if( $(this).parent().parent().parent().hasClass(subOpen) ) {
								$(infinityPushWrapper).removeClass(subOpen);
							} else {
								// reset the directParentUL width
								directParentUL.animate({
									width: navWidth - opts.spacing
								}, opts.closingspeed);
							}
							directParentUL.removeClass(inactiveList);
							directParentUL.find('ul').removeClass(inactiveList);
							directParentUL.siblings().removeClass(inactiveList);
							directParentUL.find('li').removeClass(inactiveItem);

							// Removing the close link
							directParentUL.find('.' + closeSubName).animate({
									opacity: 'hide'
								}, opts.closingspeed, 
								function() {
									$(this).remove();
								}
							);

							return false;

						} else {
						// Parent UL has not the class name, open the sub menu if exist or open the link

							if ( ( subUL.length > 0 ) && ( !subUL.is(':visible') ) ) {
							// If sub UL exist & is visible

								var getScrollPosition = directParentUL.scrollTop();

								// Adding the class names
								$(this).parent().addClass(inactiveItem);
								directParentUL.addClass(inactiveList);

								// Scrolling up function
								if(opts.autoScroll == true) {
									// Check if scroll position is not 0px
									if(getScrollPosition >= 1) {
										directParentUL.animate({ scrollTop: 0 }, opts.scrollSpeed);
									}
								}

								// Adding the close link
								if(opts.autoScroll == true) {
									// Check if scroll position is not 0px
									if(getScrollPosition >= 1) {
										$(closeSubLink).delay(opts.scrollSpeed).insertAfter($(this)).css('display', 'none').animate({
											opacity: 'show'
										}, opts.openingspeed);
									} else {
										$(closeSubLink).insertAfter($(this)).css('display', 'none').animate({
											opacity: 'show'
										}, opts.openingspeed);
									}
								} else {
									if(getScrollPosition >= 1) {
										$(closeSubLink).insertAfter($(this)).css({
											display: 'none',
											top: getScrollPosition
										}).animate({
											opacity: 'show'
										}, opts.openingspeed);
									} else {
										$(closeSubLink).insertAfter($(this)).css({
											display: 'none',
											top: 0
										}).animate({
											opacity: 'show'
										}, opts.openingspeed);
									}
								}

								// Opening animation
								if(opts.pushdirectionleft == true) {
									if(opts.autoScroll == true) {
										// Check if scroll position is not 0px
										if(getScrollPosition >= 1) {
											subUL.delay(opts.scrollSpeed).css({
												right: -(navWidth - opts.spacing)
											}).animate({
												right: 0,
												opacity: 'show',
												width: navWidth - opts.spacing
											}, opts.openingspeed);
										} else {
											subUL.css({
												right: -(navWidth - opts.spacing)
											}).animate({
												right: 0,
												opacity: 'show',
												width: navWidth - opts.spacing
											}, opts.openingspeed);
										}
									} else {
										if(getScrollPosition >= 1) {
											subUL.css({
												right: -(navWidth - opts.spacing),
												top: getScrollPosition
											}).animate({
												right: 0,
												opacity: 'show',
												width: navWidth - opts.spacing
											}, opts.openingspeed);
										} else {
											subUL.css({
												right: -(navWidth - opts.spacing),
												top: 0
											}).animate({
												right: 0,
												opacity: 'show',
												width: navWidth - opts.spacing
											}, opts.openingspeed);
										}
										
									}
								} else {
									if(opts.autoScroll == true) {
										subUL.delay(opts.scrollSpeed).css({
											left: -(navWidth - opts.spacing)
										}).animate({
											left: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									} else {
										if(getScrollPosition >= 1) {
											subUL.css({
												left: -(navWidth - opts.spacing),
												top: getScrollPosition
											}).animate({
												left: 0,
												opacity: 'show',
												width: navWidth - opts.spacing
											}, opts.openingspeed);
										} else {
											subUL.css({
												left: -(navWidth - opts.spacing),
												top: 0
											}).animate({
												left: 0,
												opacity: 'show',
												width: navWidth - opts.spacing
											}, opts.openingspeed);
										}
									}
									
								}

								// Changing the directParentUL width
								directParentUL.animate({
									width: navWidth
								}, opts.openingspeed);

								return false;

							}

						}

					} else {
					// Top UL has not the class name & the siblings has not the class name
							
						if ( ( subUL.length > 0 ) && ( !subUL.is(':visible') ) ) {
						// If sub UL exist & is visible

							var getScrollPosition = $('.' + infinityPush).scrollTop();

							// Adding the class names
							$(this).parent().addClass(inactiveItem);
							directParentUL.addClass(inactiveList);
							directParentUL.siblings().addClass(inactiveList);
							if( $(infinityPushWrapper).find('ul').is(':visible') ) {
								$(infinityPushWrapper).addClass(subOpen);
							}

							// Scrolling up function
							if(opts.autoScroll == true) {
								// Check if scroll position is not 0px
								if(getScrollPosition >= 1) {
									$('.' + infinityPush).animate({ scrollTop: 0 }, opts.scrollSpeed);
								}
							}

							// Adding the close link
							if(opts.autoScroll == true) {
								// Check if scroll position is not 0px
								if(getScrollPosition >= 1) {
									$(closeSubLink).delay(opts.scrollSpeed).insertAfter($(this)).css('display', 'none').animate({
										opacity: 'show'
									}, opts.openingspeed);
								} else {
									$(closeSubLink).insertAfter($(this)).css('display', 'none').animate({
										opacity: 'show'
									}, opts.openingspeed);
								}
							} else {
								if(getScrollPosition >= 1) {
									$(closeSubLink).insertAfter($(this)).css({
										display: 'none',
										top: getScrollPosition
									}).animate({
										opacity: 'show'
									}, opts.openingspeed);
								} else {
									$(closeSubLink).insertAfter($(this)).css({
										display: 'none',
										top: 0
									}).animate({
										opacity: 'show'
									}, opts.openingspeed);
								}
							}

							// Opening animation
							if(opts.pushdirectionleft == true) {
								// Check if autoscroll is enabled
								if(opts.autoScroll == true) {
									// Check if scroll position is not 0px
									if(getScrollPosition >= 1) {
										subUL.delay(opts.scrollSpeed).css({
											right: -(navWidth - opts.spacing)
										}).animate({
											right: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									} else {
										subUL.css({
											right: -(navWidth - opts.spacing)
										}).animate({
											right: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									}
								} else {
									if(getScrollPosition >= 1) {
										subUL.css({
											right: -(navWidth - opts.spacing),
											top: getScrollPosition
										}).animate({
											right: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									} else {
										subUL.css({
											right: -(navWidth - opts.spacing),
											top: 0
										}).animate({
											right: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									}
								}
							} else {
								if(opts.autoScroll == true) {
									subUL.delay(opts.scrollSpeed).css({
										left: -(navWidth - opts.spacing)
									}).animate({
										left: 0,
										opacity: 'show',
										width: navWidth - opts.spacing
									}, opts.openingspeed);
								} else {
									if(getScrollPosition >= 1) {
										subUL.css({
											left: -(navWidth - opts.spacing),
											top: getScrollPosition
										}).animate({
											left: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									} else {
										subUL.css({
											left: -(navWidth - opts.spacing),
											top: 0
										}).animate({
											left: 0,
											opacity: 'show',
											width: navWidth - opts.spacing
										}, opts.openingspeed);
									}
								}
							}

							return false;

						}

					}

				});

			}

		});

	};

})(jQuery);
