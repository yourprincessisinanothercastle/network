canvas = document.getElementById("canvas");

#canvas.style.width = '800px';
#canvas.style.height = '600px';
ctx = canvas.getContext('2d');

painting = document.getElementById('paint');
paint_style = getComputedStyle(painting);
canvas.width = parseInt(paint_style.getPropertyValue('width'));
canvas.height = parseInt(paint_style.getPropertyValue('height'));

mouse = {x: 0, y: 0};

canvas.addEventListener('mousemove', (e) ->
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;

, false)

ctx.lineWidth = 3;
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
ctx.strokeStyle = '#00CC99';

canvas.addEventListener('mousedown', (e) ->
  ctx.beginPath();
  ctx.moveTo(mouse.x, mouse.y);

  canvas.addEventListener('mousemove', onPaint, false);
, false)

canvas.addEventListener('mouseup', () ->
  canvas.removeEventListener('mousemove', onPaint, false);
, false)

onPaint = () ->
  append_event({
    't': 'draw',
    'coords': {
      'x': mouse.x,
      'y': mouse.y
    }
  })
  #ctx.lineTo(mouse.x, mouse.y)
  #ctx.stroke()

