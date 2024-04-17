// Function to handle drag start event
function dragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
}

// Function to handle drag over event
function dragOver(event) {
    event.preventDefault();
}

// Function to handle drop event
function drop(event) {
    event.preventDefault();
    const targetBubble = event.target;
    const draggedBubbleId = event.dataTransfer.getData('text/plain');
    const draggedBubble = document.getElementById(draggedBubbleId);

    // Ensure that the target is a valid drop zone and not the dragged bubble itself
    if (targetBubble.classList.contains('orderBubble') && draggedBubble !== targetBubble) {
        // Swap the innerHTML of the dragged bubble and the target bubble
        const temp = draggedBubble.innerHTML;
        draggedBubble.innerHTML = targetBubble.innerHTML;
        targetBubble.innerHTML = temp;
    }
}

// Add drag and drop event listeners to order bubbles
document.addEventListener('DOMContentLoaded', function() {
    const orderBubbles = document.querySelectorAll('.orderBubble');
    orderBubbles.forEach(bubble => {
        bubble.setAttribute('draggable', true);
        bubble.addEventListener('dragstart', dragStart);
    });
});

// Add drop event listener to mapped fields
document.addEventListener('DOMContentLoaded', function() {
    const mappedFields = document.querySelectorAll('.mappedFields');
    mappedFields.forEach(field => {
        field.addEventListener('dragover', dragOver);
        field.addEventListener('drop', drop);
    });
});
