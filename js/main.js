/*
|--------------------------------------------------------------------------
	AboutMe - Personal Portfolio Resume Template Main JS
|--------------------------------------------------------------------------
*/
document.addEventListener("touchstart", function() {},false);
(function ($) {
	"use strict";
	var windw = $(window);
	
	if (navigator.userAgent.match(/msie/i) || navigator.userAgent.match(/trident/i) ){
		$('body').on("mousewheel", function () {
			event.preventDefault();
			var wheelDelta = event.wheelDelta;
			var currentScrollPosition = window.pageYOffset;
			window.scrollTo(0, currentScrollPosition - wheelDelta);
		});
	}
	
/*
|--------------------------------------------------------------------------
	carousel
|--------------------------------------------------------------------------
*/
	//Main home Slider
	$('#home-carousel').owlCarousel({
		items: 1,
		autoplay: true,
		dots: false,
		nav: true,
		navText: ["&#10094;", "&#10095;"],
		slideSpeed : 300,
		loop: true,
		smartSpeed:450
	});
		
	//Blog Carousel
	$('#blog .owl-carousel').owlCarousel({
	   autoplay: false,
	   margin: 30,
	   nav: true,
	   navText: ["&#10094;", "&#10095;"],
	   loop: true,
	   responsive: {
				  0: {
					items: 1
				  },
				  534: {
					items: 2
				  },
				  992: {
					items: 3
				  }
				}
	});
	
	//Testimonial Carousel single column
	$('.testimonial-single .owl-carousel').owlCarousel({
	   items: 1,
	   autoplay: true,
	   margin: 30,
	   loop: true,
	   nav: false,
	   navText: ["&#10094;", "&#10095;"]
	});
	
	//clients Carousel
	$('#clients .owl-carousel').owlCarousel({
	   autoplay: true,
	   margin: 30,
	   loop: true,
	   dots: false,
	   nav: false,
	   navText: ["&#10094;", "&#10095;"],
	   responsive: {
				  0: {
					items: 1
				  },
				  300: {
					items: 2
				  },
				  480: {
					items: 3
				  },
				  641: {
					items: 4
				  },
				  1024: {
					items: 6
				  }
				}
	});
	
/*
|--------------------------------------------------------------------------
	Typewrite
|--------------------------------------------------------------------------
*/	
	var TxtType = function(el, toRotate, period) {
        this.toRotate = toRotate;
        this.el = el;
        this.loopNum = 0;
        this.period = parseInt(period, 10) || 2000;
        this.txt = '';
        this.tick();
        this.isDeleting = false;
    };

    TxtType.prototype.tick = function() {
        var i = this.loopNum % this.toRotate.length;
        var fullTxt = this.toRotate[i];

        if (this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

        var that = this;
        var delta = 200 - Math.random() * 100;

        if (this.isDeleting) { delta /= 2; }

        if (!this.isDeleting && this.txt === fullTxt) {
        delta = this.period;
        this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        this.loopNum++;
        delta = 500;
        }

        setTimeout(function() {
        that.tick();
        }, delta);
    };

    window.onload = function() {
        var elements = document.getElementsByClassName('typewrite');
        for (var i=0; i<elements.length; i++) {
            var toRotate = elements[i].getAttribute('data-type');
            var period = elements[i].getAttribute('data-period');
            if (toRotate) {
              new TxtType(elements[i], JSON.parse(toRotate), period);
            }
        }
        // INJECT CSS
        var css = document.createElement("style");
        css.type = "text/css";
        css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
        document.body.appendChild(css);
    };
	
/*
|--------------------------------------------------------------------------
	ACTIVE STICKY HEADER
|--------------------------------------------------------------------------
*/	
	var navh = $('.header-nav');
	var scrollp = windw.scrollTop();		
	if (scrollp > 100) {
		navh.addClass("menu-bg");
	} else {
		navh.removeClass("menu-bg");
	}
	windw.scroll(function () {
		if ($(this).scrollTop() > 100) {
			navh.addClass("menu-bg");
		} else {
			navh.removeClass("menu-bg");
		}
	});
	
/*
|--------------------------------------------------------------------------
	Change Active State on Scroll
|--------------------------------------------------------------------------
*/		
	var sections = $('section')
	  , nav = $('nav')
	  , nav_height = nav.outerHeight();
	 
	windw.on('scroll', function () {
	  var cur_pos = $(this).scrollTop();
	 
	  sections.each(function() {
		var top = $(this).offset().top - (nav_height-24),
			bottom = top + $(this).outerHeight();
	 
		if (cur_pos >= top && cur_pos <= bottom) {
		  nav.find('a').removeClass('active');
		  sections.removeClass('active');
	 
		  $(this).addClass('active');
		  nav.find('a[href="#'+$(this).attr('id')+'"]').addClass('active');
		}
	  });
	});
	
/*
|--------------------------------------------------------------------------
	Smoth Scroll
|--------------------------------------------------------------------------
*/
	$(document).on('click', 'a[href*="#"]:not([href="#"])', function(event){
	  if (location.pathname.replace(/^\//,'') === this.pathname.replace(/^\//,'') && location.hostname === this.hostname) {
		var target = $(this.hash);
		target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
		
		var topBar_height = $('.TopBar').outerHeight() - 3;
		if(!topBar_height)
			topBar_height = 0;
		
		var header_height = 50 + topBar_height;
		
		if (target.length) {
		  $('html, body').animate({
			scrollTop: target.offset().top - header_height
		  }, 1000);
		  return false;
		}
	  }
	});
	
/*
|--------------------------------------------------------------------------
	Circle Progress Bar
|--------------------------------------------------------------------------
*/
	windw.on('load', function() {
		function animateElements() {
			$('.progressbar').each(function () {
				var elementPos = $(this).offset().top;
				var topOfWindow = windw.scrollTop();
				var percent = $(this).find('.circle').attr('data-percent');
				var barColor = $(this).find('.circle').attr('data-color');
				var percentage = parseInt(percent, 10) / parseInt(100, 10);
				var animate = $(this).data('animate');
				if (elementPos < topOfWindow + windw.height() - 30 && !animate) {
					$(this).data('animate', true);
					$(this).find('.circle').circleProgress({
						startAngle: -Math.PI / 2,
						value: percent / 100,
						size: 120,
						thickness: 14,
						fill: {
							color: barColor
						},
						animation: {
							duration: 3000,
							easing: 'circleProgressEasing'
						}
					}).on('circle-animation-progress', function (event, progress, stepValue) {
						$(this).find('div').text((stepValue*100).toFixed(1) + "%");
					}).stop();
				}
			});
		}
		// Show animated elements
		animateElements();
		windw.scroll(animateElements);
	});

/*
|--------------------------------------------------------------------------
	isotope Filter Start
|--------------------------------------------------------------------------
*/
	var myTheme = window.myTheme || {},
	$win = $( window );
	
	myTheme.Isotope = function () {	
		// 4 column layout
		var isotopeContainer = $('.isotopeContainer');
		if( !isotopeContainer.length || !jQuery().isotope ) return;
		$win.on('load', function() {
			isotopeContainer.isotope({
				itemSelector: '.isotopeSelector'
			});
			$('.isotopeFilters').on( 'click', 'a', function(e) {
				$('.isotopeFilters').find('.active').removeClass('active');
				$(this).parent().addClass('active');
				var filterValue = $(this).attr('data-filter');
				isotopeContainer.isotope({ filter: filterValue });
				e.preventDefault();
			});
		});		
	};	
	myTheme.Isotope();
	
/*
|--------------------------------------------------------------------------
	Lighbox
|--------------------------------------------------------------------------
*/
	lightbox.option({
      'albumLabel': "Item %1 of %2",
      'positionFromTop': 40,
      'resizeDuration': 500,
      'disableScrolling': false
    });
	
	if( $(document.body).width() > 1200 ) {
		lightbox.option({
		  'disableScrolling': true
		});
	}
	
	windw.resize(function() {
		
		if( $(document.body).width() < 1200 ) {
			$(".lb-dataContainer").css("width", "80%");
			$(".lb-dataContainer").css("height", "80%");
			$(".lb-outerContainer").css("width", "80%");
			$(".lb-outerContainer").css("height", "80%");
			$(".lb-image").css("width", "100%");
			$(".lb-image").css("height", "100%");
		}

	});

/*
|--------------------------------------------------------------------------
	Subscribe Form
|--------------------------------------------------------------------------
*/	
	//Change YOUR MAILCHIMP ACCOUNT LIST FORM ACTION URL
	$('#mc-form').ajaxChimp({
		url: 'http://YOUR MAILCHIMP ACCOUNT LIST FORM ACTION'
	});

/*
|--------------------------------------------------------------------------
	Quote Form
|--------------------------------------------------------------------------
*/	
	$("#quoteForm").validator().on("submit", function (event) {
		if (event.isDefaultPrevented()) {
			//handle the invalid form...
			formError();
			submitQuoteMSG(false, "Please fill in the form properly!");
		} else {
						
			var filter = /^((\+[1-9]{1,4}[ \-]*)|(\([0-9]{2,3}\)[ \-]*)|([0-9]{2,4})[ \-]*)*?[0-9]{3,4}?[ \-]*[0-9]{3,4}?$/;
			
			if (filter.test($("#quotePhone").val())) {
				//everything looks good!
				event.preventDefault();
				submitquoteForm();
			}	
			else {	
				submitQuoteMSG(false, "Please enter valid phone");
				return false;
			}
			
		}
	});
	
	function submitquoteForm(){
		$.ajax({
			type: "POST",
			url: "quote-process.php",
			data: $( "#quoteForm" ).serialize(),
			success : function(text){
				if (text == "success"){
					quoteFormSuccess();
				} else {
					formError();
					submitQuoteMSG(false,text);
				}
			}
		});
	}
	
	function quoteFormSuccess(){
		$("#quoteForm")[0].reset();
		submitQuoteMSG(true, "Your Quote Request Submitted Successfully!")
	}
	
	function submitQuoteMSG(valid, msg){
		if(valid){
			var msgClasses = "h3 text-center text-success";
		} else {
			var msgClasses = "h3 text-center text-danger";
		}
		$("#msgQuoteSubmit").removeClass().addClass(msgClasses).text(msg);
		$('html,body').animate({
			scrollTop: $("#msgQuoteSubmit").offset().top - 80},
        'slow');
	}	

/*
|--------------------------------------------------------------------------
	Contact Form
|--------------------------------------------------------------------------
*/	
	$("#contactForm").validator().on("submit", function (event) {
		if (event.isDefaultPrevented()) {
			//handle the invalid form...
			formError();
			submitContactMSG(false, "Please fill in the form properly!");
		} else {
			
			var filter = /^((\+[1-9]{1,4}[ \-]*)|(\([0-9]{2,3}\)[ \-]*)|([0-9]{2,4})[ \-]*)*?[0-9]{3,4}?[ \-]*[0-9]{3,4}?$/;
			
			if (filter.test($("#phone").val())) {
				//everything looks good!
				event.preventDefault();
				submitcontactForm();
			}	
			else {	
				submitContactMSG(false, "Please enter valid phone");
				return false;
			}
			
		}
	});
	
	function submitcontactForm(){
		$.ajax({
			type: "POST",
			url: "contact-process.php",
			data: $( "#contactForm" ).serialize(),
			success : function(text){
				if (text == "success"){
					contactFormSuccess();
				} else {
					formError();
					submitContactMSG(false,text);
				}
			}
		});
	}
	
	function contactFormSuccess(){
		$("#contactForm")[0].reset();
		submitContactMSG(true, "Your Message Submitted Successfully!")
	}
	
	function formError(){
		$(".help-block.with-errors").removeClass('hidden');
	}
	
	function submitContactMSG(valid, msg){
		if(valid){
			var msgClasses = "h3 text-center text-success";
		} else {
			var msgClasses = "h3 text-center text-danger";
		}
		$("#msgContactSubmit").removeClass().addClass(msgClasses).text(msg);
		$('html,body').animate({
			scrollTop: $("#msgContactSubmit").offset().top - 80},
        'slow');
	}

/*
|--------------------------------------------------------------------------
	Accordion
|--------------------------------------------------------------------------
*/
	function toggleChevron(e) {
		$(e.target)
			.prev('.panel-heading')
			.find("i.indicator")
			.toggleClass('glyphicon-plus glyphicon-minus');
		
		$('#accordion .panel-heading').toggleClass('highlight default-color');
		$(e.target).prev('.panel-heading').addClass('highlight');
		
	}
	$('#accordion').on('hidden.bs.collapse', toggleChevron);
	$('#accordion').on('shown.bs.collapse', toggleChevron);

/*
|--------------------------------------------------------------------------
| CountUp
|--------------------------------------------------------------------------
*/
	$('.counter').counterUp({
		delay: 5,
		time: 1000
	});

/*
|--------------------------------------------------------------------------
	Scrollup
|--------------------------------------------------------------------------
*/
	var scrollup = $('.scrollup');
	windw.scroll(function () {
		if ($(this).scrollTop() > 100) {
			scrollup.fadeIn();
		} else {
			scrollup.fadeOut();
		}
	});
	scrollup.on('click', '', function(event){
		$("html, body").animate({
			scrollTop: 0
		}, 600);
		return false;
	});

})(jQuery);
	
/*
|--------------------------------------------------------------------------
	End
|--------------------------------------------------------------------------
*/