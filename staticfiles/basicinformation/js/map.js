visible() && !$(ct).hasClass('animated')) {
            $(ct).countTo({
                speed: 2000
            });
            $(ct).addClass('animated');
        }
    }

    function initCountTo() {
        var counter = $('.count');
        counter.each(function () {
            animateCountTo(this);
        });
    }

    initCountTo();

    /*-----------------------------------------------------
    Banner Slider 2
    ------------------------------------------------------*/
    $('.testimonial-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        dots: true,
        fade: true,
        asNavFor: '.testimonial-banner-slider'
    });
    $('.testimonial-banner-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: '.testimonial-slider',
        arrows: false,
        focusOnSelect: true,
        autoplay: true,
        autoplaySpeed: 2000
    });

    /*-----------------------------------------------------
    Countdown 
    ------------------------------------------------------*/
    $('.countdown').each(function () {
        var endTime = $(this).data('time');
        $(this).countdown(endTime, function (tm) {
            var countTxt = '';
            countTxt += '<span class="section_count"><span class="section_count_da