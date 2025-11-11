import os
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from django.conf import settings
from django.core.cache import cache

class LSTMPredictor:
    """
    Servicio que encapsula toda la lógica del modelo LSTM.
    Maneja carga, escalado, predicción y validación.
    """
    
    # Configuración del modelo
    L_MAX = 73  # timesteps
    N_FEATURES = 135  # características
    
    # Rutas de archivos (desde settings)
    MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models/lstm_model_rendimiento.keras')
    SCALER_X_PATH = os.path.join(settings.BASE_DIR, 'ml_models/scaler_X.pkl')
    SCALER_Y_PATH = os.path.join(settings.BASE_DIR, 'ml_models/scaler_Y.pkl')
    DATA_BASE_PATH = os.path.join(settings.BASE_DIR, 'ml_models/df_base_cronologico.csv')
    
    _modelo = None
    _scaler_x = None
    _scaler_y = None
    _datos_historicos = None

    @classmethod
    def _cargar_recursos(cls):
    #""Carga modelo y scalers desde archivos""
        if cls._modelo is None:
          cls._modelo = tf.keras.models.load_model(cls.MODEL_PATH)
        if cls._scaler_x is None:
          cls._scaler_x = joblib.load(cls.SCALER_X_PATH)
        if cls._scaler_y is None:
          cls._scaler_y = joblib.load(cls.SCALER_Y_PATH)
    
    @classmethod
    def _cargar_datos_historicos(cls):
        """Carga el CSV de datos históricos"""
        if cls._datos_historicos  is None:
            # Ruta relativa (correcta)
            csv_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data',
                'df_base_cronologico.csv'
            )
            
            if os.path.exists(csv_path):
                cls._datos_historicos  = pd.read_csv(csv_path)
            else:
                raise FileNotFoundError(f"CSV no encontrado: {csv_path}")
        
        return cls._datos_historicos 
    
    @classmethod
    def obtener_historico_medias(cls):
        """Retorna el promedio histórico de features."""
        df = cls._cargar_datos_historicos()  
        feature_cols = [col for col in df.columns
                    if col not in ['Date', 'Rendimiento']]
        return df[feature_cols].mean().values
    
    @classmethod
    def generar_datos_simulados(cls, trend_shift=1.05, noise_level=0.15, year_offset=0):
        """
        Genera datos climáticos simulados con tendencia y ruido.
        
        Args:
            trend_shift: Factor de tendencia (1.05 = +5%)
            noise_level: Nivel de ruido (0.15 = ±15%)
            year_offset: Desplazamiento de años (para multi-año)
        
        Returns:
            np.ndarray de forma (L_MAX, N_FEATURES)
        """
        historicos = cls.obtener_historico_medias()
        
        # Aplicar tendencia progresiva
        annual_trend = trend_shift + (year_offset * 0.005)
        X_base = np.tile(historicos, (cls.L_MAX, 1))
        X_trend = X_base * annual_trend
        
        # Aplicar ruido controlado
        noise_range = np.abs(historicos) * noise_level
        noise = np.random.uniform(
            low=-noise_range,
            high=noise_range,
            size=(cls.L_MAX, cls.N_FEATURES)
        )
        
        return X_trend + noise
    
    
    
    @classmethod
    def predecir(cls, datos_entrada_raw):
        """
        Realiza predicción sobre datos en escala original.
        
        Args:
            datos_entrada_raw: np.ndarray (73, 135) en escala original
        
        Returns:
            dict con predicción y metadata
        """
        cls._cargar_recursos()
        
        try:
            # Normalizar
            X_scaled = cls._scaler_x.transform(datos_entrada_raw)
            X_input = X_scaled.reshape(1, cls.L_MAX, cls.N_FEATURES)
            
            # Inferencia
            prediccion_scaled = cls._modelo.predict(X_input, verbose=0)
            
            # Desescalar
            prediccion_real = cls._scaler_y.inverse_transform(prediccion_scaled)
            rendimiento = float(prediccion_real[0][0])
            
            return {
                'success': True,
                'rendimiento': rendimiento,
                'confianza': 0.85,  # Placeholder
                'error': None
            }
        
        except Exception as e:
            return {
                'success': False,
                'rendimiento': None,
                'error': str(e)
            }
    
    @classmethod
    def predecir_multiples_anos(cls, anos=10, trend_shift=1.05, noise_level=0.15):
        """
        Genera predicciones para múltiples años.
        
        Returns:
            list[dict] con predicción por año
        """
        results = []
        for i in range(anos):
            X_sim = cls.generar_datos_simulados(
                trend_shift=trend_shift,
                noise_level=noise_level,
                year_offset=i
            )
            pred = cls.predecir(X_sim)
            pred['ano'] = 2024 + i
            results.append(pred)
        return results
