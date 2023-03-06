$(document).ready(function () {

  $('#sknn').click(function(){
    console.log("sknn click...")
    window.location.href="example.html"
  })

  $('#slcss').click(function(){
    console.log("slcss click..")
    $.ajax({
      type: 'get',
      url: 'localhost:7995/slcss',
    })
  })

  $('#sdtw').click(function(){
    console.log("sdtw click...")
    $.ajax({
      type: 'get',
      url: 'localhost:7995/sdtw',
    })
  })

  $('#sbd').click(function(){
    console.log("sbd click...")
    $.ajax({
      type: 'get',
      url: 'localhost:7995/sbd',
    })
  })

})