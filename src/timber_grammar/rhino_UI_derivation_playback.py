import compas
from assembly_model import Model
from Derivation import Derivation

import rhinoscriptsyntax as rs
from compas_rhino.artists import MeshArtist

__commandname__ = "derivation_playback"

def RunCommand(is_interactive):

    #load Derivation and delete last step
    derivation = Derivation.from_json("derivation.json")

    continue_playback = True
    while(continue_playback):
        #ask user for which step they would like to see
        derivation_last_step_index = derivation.count - 1
        
        step_id = rs.GetInteger("Enter which step to visualize (0 - "+ str(derivation_last_step_index) + " step) (Enter -1 for last step)", None, -1, derivation_last_step_index)
        if (step_id == -1): step_id = derivation_last_step_index
        if (step_id == None): break # Allow user to quite the command

        #load the selected model
        model = derivation.get_step(step_id)

        #Visualization 
        artist = MeshArtist(None, layer ='BEAM::Beams_out')
        artist.clear_layer()
        for beam in model.beams:
            artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')
            artist.draw_faces(join_faces=True)
        artist.redraw()           

if __name__ == '__main__':
    RunCommand(True)