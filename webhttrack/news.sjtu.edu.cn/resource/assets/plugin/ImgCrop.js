		$img.css('width','auto');

		$w = $img.width();
		$h = $img.height();

		$bw = $(this).width();
		$bh = $(this).height();

		b1 = $w / $h;
		b2 = $bw / $bh;

		if (b1 > b2) {

			$img.css("height", "100%")
			$wed = $bh * b1;
			$img.css("width", $wed + "px")
			fz = ($(this).width() - $wed) / 2;
			$img.css("margin-left", fz + "px")

		} else {
			$img.css("width", "100%")
			$hed = $bw / b1;
			$img.css("height", $hed + "px")
			fs = ($(this).height() - $hed) / 2;
			$img.css("margin-top", fs + "px")
		}
	});
};

window.onload = function () {
