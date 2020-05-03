import eli5
from eli5.sklearn import PermutationImportance
from matplotlib import pyplot as plt
from pdpbox import pdp, get_dataset, info_plots
import shap


class CheckFeatureImportance:
    '''Feature eng methods'''

    def __init__(self, X, y):
        self.X, self.y = X, y

    def permutation_importance(self, model, X_val, y_val):
        '''check Feature importance on the Validation data for the fitted model'''
        perm = PermutationImportance(model, random_state=1).fit(X_val, y_val)
        return eli5.show_weights(perm, feature_names = X_val.columns.tolist())

    def pdp_plot(self, model, X_val, feature_to_plot):
        '''plot partial dependence for list of variables.
        model: fitted model
        X_val: validation dataset
        feature_to_plot : list of features
        '''
        for feat_name in feature_to_plot:
            pdp_dist = pdp.pdp_isolate(model, X_val, X_val.columns.tolist(), feat_name)
            pdp.pdp_plot(pdp_dist, feat_name)
            plt.show()

    def pdp_plot_bivariate(self, model, X_val, feature_pair):
        ''' pdp plot for feature pair
        model: fitted model
        X_val: validation dataset
        feature_pair : pair of feature (list)
        '''
        partial_plot  =  pdp.pdp_interact(model, X_val,
                                                     X_val.columns.tolist(), feature_pair)
        pdp.pdp_interact_plot(partial_plot, feature_pair, plot_type='contour')
        plt.show()

    def shap_value_plot(self, model, val_X, base_observation, kind='default'):
        '''
        ToDo: refer to github page... add all plots https://github.com/slundberg/shap
        val_X: validation data
        base_observation: index of observation in val_X; to be used for prediction
                          could use multiple rows if desired.
        
        
        '''
        data_for_prediction = val_X.iloc[base_observation]  
        data_for_prediction_array = data_for_prediction.values.reshape(1, -1)
        model.predict_proba(data_for_prediction_array)
        if kind=='default':
            if type(model) is RandomForestClassifier:
                explainer = shap.TreeExplainer(model)
                # Calculate Shap values
                shap_values = explainer.shap_values(data_for_prediction)
                shap.initjs()
                return shap.force_plot(explainer.expected_value[1], shap_values[1], data_for_prediction)
            elif type(model) is LinearRegression:
                raise NotImplementedError

            else: #works for all type of models...
                # use Kernel SHAP to explain test set predictions
                k_explainer = shap.KernelExplainer(model.predict_proba, val_X)
                k_shap_values = k_explainer.shap_values(data_for_prediction)
                return shap.force_plot(k_explainer.expected_value[1], k_shap_values[1], data_for_prediction)
        elif kind=='summary':
            return shap.summary_plot(shap_values)
        elif kind=='train_summary':
            # visualize the training set predictions
            shap.force_plot(explainer.expected_value, shap_values, X)
        else:
            return None



    def shap_dependence_contib_plot(self, model, X_val):
        '''
        ToDo: check and complete code
        refer to https://www.kaggle.com/dansbecker/advanced-uses-of-shap-values
        and 
        https://www.kaggle.com/shubhamsoni45/exercise-advanced-uses-of-shap-values/edit
        '''

        # Create object that can calculate shap values
        explainer = shap.TreeExplainer(my_model)

        # calculate shap values. This is what we will plot.
        shap_values = explainer.shap_values(X)

        # make plot.
        shap.dependence_plot('Ball Possession %', shap_values[1], X, interaction_index="Goal Scored")