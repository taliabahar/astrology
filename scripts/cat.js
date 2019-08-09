window.onload = function() {
    let speed = 150;
    let i = 0;
    let cat = document.getElementById("cat_img");
    cat.addEventListener('click', meow);
    meow_sound = document.getElementById("meow_sound");
    txt = "Hi! I'm Phillipe the good advice cat!"

    function meow(event) {
      meow_sound.play();
      getAdvice();
      document.getElementById("text").innerHTML = txt;
      console.log(txt);
      // animationEffect();
      // typeWriter();
    }

  function getAdvice() {
    const url = 'https://api.adviceslip.com/advice'; // Get one piece of advice
    fetch(url)
      .then((resp) => resp.json())
      .then(function(data) {
        let advice = data["slip"]["advice"];
        txt = advice;
    });
  }

  // function typeWriter() {
  //   if (i < txt.length) {
  //     document.getElementById("text").innerHTML += txt.charAt(i);
  //     i++;
  //     setTimeout(typeWriter, speed);
  //   }
  //   if (txt.charAt(i) === "|") {
  //     i++;
  //     document.getElementById("text").innerHTML = "";
  //   }
  // }

  function animationEffect() {
    let spanWidth = $('#text').width();
    $('#text').animate( { width: spanWidth }, 3000 );
  }

}
