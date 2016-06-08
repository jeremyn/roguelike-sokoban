# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import os
import shutil
import pickle
import time
import constants as const


class CorruptHighScoreFileError(Exception):

    pass

class HighScoreFileHandlingError(Exception):
    
    pass

class HighScores(object):
    
    def __init__(self, 
                 hs_file_name = const.DEFAULT_HIGH_SCORE_FILE_NAME_FULL):
        self.hs_file_name = hs_file_name
        self.scores = {}
        try:
            if os.path.isfile(self.hs_file_name):
                hs_file = open(self.hs_file_name, "rb")
                self.scores = pickle.load(hs_file)
        except IOError:
            reason = "could not open high score file \'%s\'." % \
                    self.hs_file_name
            raise HighScoreFileHandlingError(reason)
        except (pickle.UnpicklingError, AttributeError, EOFError, ImportError,
                IndexError):
            reason = "corrupt high score file \'%s\'." % self.hs_file_name
            raise CorruptHighScoreFileError(reason)        
    
    def get_high_score(self, file_name, level_name):
        file_name = os.path.split(file_name)[1]
        try:
            return self.scores[file_name][level_name]
        except KeyError:
            return 0

    def set_high_score(self, file_name, level_name, score):
        file_name = os.path.split(file_name)[1]
        if self.scores.has_key(file_name):
            self.scores[file_name][level_name] = score
        else:
            self.scores[file_name] = {level_name: score}
            
    def save_high_scores(self, hs_file_name = None):
        if hs_file_name is None:
            hs_file_name = self.hs_file_name
        
        timestamp = "".join(str(time.time()).split("."))
        temp_backup_file_name = os.path.join(os.path.split(hs_file_name)[0],
                                             "temp" + timestamp + \
                                             const.HIGH_SCORE_EXTENSION)

        try:
            if os.path.isfile(hs_file_name):
                shutil.copy(hs_file_name, temp_backup_file_name)
        except (shutil.Error, IOError):
            reason = "could not create backup for high score file \'%s\' "\
                     "before saving high scores. Current high score file is "\
                     "preserved." % hs_file_name
            raise HighScoreFileHandlingError(reason)
        
        try:
            hs_file = open(hs_file_name, "wb")
        except IOError:
            if not os.path.isfile(hs_file_name):
                reason = "could not create high score file \'%s\'." % \
                        hs_file_name
            else:
                reason = "could not open high score file \'%s\' for writing."%\
                        hs_file_name
            try:
                if os.path.isfile(temp_backup_file_name):
                    os.unlink(temp_backup_file_name)
            except OSError:
                reason += " Also could not delete high score backup file "\
                          "\'%s\'." % temp_backup_file_name
                raise HighScoreFileHandlingError(reason)
            raise HighScoreFileHandlingError(reason)
        
        try:
            pickle.dump(self.scores, hs_file)
        except (pickle.PickleError, AttributeError, EOFError, ImportError,
                IndexError):
            reason = "could not save current high score data to file "\
                     "\'%s\'. Your current high score data can be restored "\
                     "from file \'%s\'." % (hs_file_name,
                                            temp_backup_file_name)
            raise Exception(reason)
        hs_file.close()
 
        try:
            if os.path.isfile(temp_backup_file_name):
                os.unlink(temp_backup_file_name)
        except OSError:
            reason = "could not delete high score backup file \'%s\'." % \
                    temp_backup_file_name
            raise HighScoreFileHandlingError(reason)
