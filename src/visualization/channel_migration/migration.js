window.onload = function () {
    var canvas = $('#myCanvas');
    paper.setup(canvas);

    var path = new Path.Circle({
        center: view.center,
        radius: 30,
        strokeColor: 'black'
    });

    paper.view.draw();
};

function onResize(event) {
    // whenever the window is resized, recenter the path
    path.position = view.center;
}
