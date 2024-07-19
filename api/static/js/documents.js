// documents.js

// PDF.js initialization
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://mozilla.github.io/pdf.js/build/pdf.js';

// Google Viewer initialization
function initGoogleViewer(fileUrl) {
  var viewerUrl = 'https://docs.google.com/viewer?url=' + encodeURIComponent(fileUrl) + '&embedded=true';
  $('#document-viewer').html('<iframe src="' + viewerUrl + '" width="100%" height="100%" frameborder="0"></iframe>');
}

// PDF viewer function
function viewPdf(fileUrl) {
  pdfjsLib.getDocument(fileUrl).promise.then(function(pdf) {
    pdf.getPage(1).then(function(page) {
      var scale = 1.5;
      var viewport = page.getViewport({ scale: scale });
      var canvas = document.getElementById('document-viewer');
      var context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      var renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      page.render(renderContext);
    });
  }).catch(function(error) {
    console.error('Error while loading PDF:', error);
  });
}

// Document viewer function
function viewDocument(fileUrl, fileType) {
  $('#documentModal').modal('show');
  if (fileType.includes('pdf')) {
    viewPdf(fileUrl);
  } else if (fileType.includes('word') || fileType.includes('powerpoint')) {
    initGoogleViewer(fileUrl);
  } else {
    $('#document-viewer').html('<p>Sorry, this file type is not supported for viewing.</p>');
  }
}

// Event listener for document view
$('.view-document').click(function() {
  var fileUrl = $(this).data('file-url');
  var fileType = $(this).data('file-type');
  viewDocument(fileUrl, fileType);
});



document.addEventListener('DOMContentLoaded', function() {
  const downloadButtons = document.querySelectorAll('.btn-download');
  const spinner = new Spinner({
    color: '#28ce03',
    lines: 12,
    length: 8,
    radius: 10,
    width: 3,
    zIndex: 2e9,
    top: '50%',
    left: '50%',
    hwaccel: true,
  });

  downloadButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault();
      const fileUrl = this.getAttribute('href');
      showSpinner();
      setTimeout(function() {
        window.location.href = fileUrl;
        hideSpinner();
      }, 1000); // Simulating a delay for demonstration purposes
    });
  });

  function showSpinner() {
    spinner.spin(document.body);
  }

  function hideSpinner() {
    spinner.stop();
  }
});