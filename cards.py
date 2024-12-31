from nicegui import ui
def default():
  return ui.card(align_items=['center']).classes('fixed-center').style(
      'max-width: 90vw;'  # Set the max width of the card
      'max-height: 90vh;'  # Ensure the max height is 90% of the viewport height
      'overflow: auto;'  # Allow scrolling inside the card if content overflows
      'display: flex;'  # Use flexbox for centering
      'flex-direction: column;'  # Stack content vertically
      'justify-content: flex-start;'
      'align-items: center;'
  )
