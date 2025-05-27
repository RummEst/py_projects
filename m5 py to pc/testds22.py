import tedst2 as gg
import time

gui = gg.aiGUI()
# This will create a popup while the main code keeps running
gui.create_notification_popup(title="Listening...", use_comment=False)
time.sleep(5)
#gui.kill_all_popups()
#del gui
gui = gg.aiGUI()
# This will create a popup while the main code keeps running
gui.create_notification_popup(title="Thinking...", comment="Kui pede on karlis?")
time.sleep(5)
#gui.kill_all_popups()
#del gui
gui = gg.aiGUI()
# This will create a popup while the main code keeps running
gui.create_notification_popup(title="Response", comment="Väga pede frl ongod")
